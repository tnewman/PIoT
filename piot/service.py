from contextlib import contextmanager
from datetime import datetime, timedelta

import logging, schedule, time
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from piot import config
from piot.sensor import SensorClasses
from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor
from piot.model import NotificationEvent, AnalogSensorReading, DigitalSensorReading, SensorReading
from piot.notification import TwilioSMSNotification

logger = logging.getLogger(__name__)

engine = create_engine(config.sql_alchemy_connection_string)


@contextmanager
def transaction_scope():
    """ Wraps SQLAlchemy operations. Commits a session if there are no errors,
        rolls back a session on exception and closes a session in either case.
    """
    session_class = sessionmaker(bind=engine, expire_on_commit=False)
    session = session_class()
    
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class BaseSQLAlchemyService:
    """ Base Class providing CRUD (Create, Read, Update and Delete) operations
        to all services that rely on SQLAlchemy.
    """

    def __init__(self, model):
        """ Constructor
        :param model: Model Class used by child service.
        :type model: piot.model.Base
        """
        self._model = model
    
    def all(self):
        """ Retrieve all records.
        :return: All records.
        :rtype model: piot.model.Base
        """
        with transaction_scope() as session:
            records = session.query(self._model).with_polymorphic('*').all()

        return records
    
    def get(self, key):
        """ Retrieves a specific record.
        :param key: Primary Key of record to retrieve.
        :return: Record specified by the id.
        :rtype model: piot.model.Base
        """
        with transaction_scope() as session:
            record = session.query(self._model).with_polymorphic('*') \
                .filter_by(id=key).first()

        return record

    def create(self, object):
        with transaction_scope() as session:
            session.add(object)

    def update(self, object):
        with transaction_scope() as session:
            session.merge(object)
    
    def delete(self, object):
        with transaction_scope() as session:
            session.delete(object)


class NotificationPersistenceService(BaseSQLAlchemyService):
    def __init__(self):
        super().__init__(NotificationEvent)

    def get_newest_notification(self, sensor_name):
        with transaction_scope() as session:
            result = session.query(
                    NotificationEvent, SensorReading) \
                    .filter(SensorReading.id == NotificationEvent.sensor_id) \
                    .filter(SensorReading.name == sensor_name) \
                    .order_by(desc(NotificationEvent.timestamp)).first()

        if result:
            notification, reading = result
            return notification
        else:
            return None


class SensorReadingPersistenceService(BaseSQLAlchemyService):
    def __init__(self):
        super().__init__(SensorReading)


class SensorReadingSchedulingService:
    def __init__(self, sensor_class=SensorClasses,
                 sms_notification=TwilioSMSNotification):
        self.sensor_class = sensor_class()
        self.sensor_persistence = SensorReadingPersistenceService()
        self.notification_persistence = NotificationPersistenceService()
        self.sms_notification = sms_notification()

    def run_jobs(self):
        schedule.every(30).seconds.do(self._sensor_reading_job)
        self._sensor_reading_job()

        while True:
            schedule.run_pending()
            time.sleep(1)

    def _sensor_reading_job(self):
        for sensor_class in self.sensor_class.get_all_sensor_classes():
            try:
                if issubclass(sensor_class, BaseAnalogSensor):
                    self._read_analog_sensor(sensor_class())
                elif issubclass(sensor_class, BaseDigitalSensor):
                    self._read_digital_sensor(sensor_class())
            except Exception:
                logger.exception('Failed to read sensor ' +
                                 sensor_class.__name__)

    def _read_analog_sensor(self, analog_sensor):
        value = analog_sensor.read_analog_sensor()

        analog_reading = AnalogSensorReading()
        analog_reading.name = analog_sensor.sensor_name
        analog_reading.value = value
        analog_reading.unit = analog_sensor.unit
        analog_reading.timestamp = datetime.now()
        self.sensor_persistence.create(analog_reading)

        if value != analog_sensor.error_sentinel:
            if value < analog_sensor.min_normal or \
                    value > analog_sensor.max_normal:
                logger.info(analog_reading.name + ' Analog Sensor Value: ' +
                            str(analog_reading.value) + analog_reading.unit +
                            ' - Out of Normal Range')
                self._send_notification(
                    analog_sensor, analog_reading)
            else:
                logger.info(analog_reading.name + ' Analog Sensor Value: ' +
                            str(analog_reading.value) + analog_reading.unit +
                            ' - Within Normal Range')
        else:
            logger.info(analog_reading.name + ' Analog Sensor Value: ' +
                        str(analog_reading.value) + analog_reading.unit +
                        ' - Error Sentinel - Ignoring')

    def _read_digital_sensor(self, digital_sensor):
        value = digital_sensor.read_digital_sensor()

        digital_reading = DigitalSensorReading()
        digital_reading.name = digital_sensor.sensor_name
        digital_reading.value = value
        digital_reading.timestamp = datetime.now()
        self.sensor_persistence.create(digital_reading)

        if value != digital_sensor.normal_value:
            logger.info(digital_reading.name + ' Digital Sensor Value: ' +
                        str(digital_reading.value) +
                        ' - Out of Normal Range')

            self._send_notification(digital_sensor, digital_reading)
        else:
            logger.info(digital_reading.name + ' Digital Sensor Value: ' +
                        str(digital_reading.value) +
                        ' - Within Normal Range')

    def _send_notification(self, notification_sensor, reading):
        last_notification = self.notification_persistence \
            .get_newest_notification(reading.name)

        if last_notification is None:
            send_notification = True
        elif reading.timestamp > last_notification.timestamp + \
                timedelta(days=1):
            send_notification = True
        else:
            send_notification = False

        if send_notification:
            try:
                self.sms_notification.send_notification(
                        notification_sensor.notification_text)
                notification_event = NotificationEvent()
                notification_event.sensor_id = reading.id
                notification_event.timestamp = datetime.now()
                self.notification_persistence.create(notification_event)
                logger.info(reading.name + ' - Sent Notification')
            except IOError:
                logger.exception(
                        reading.name + ' - Failed to send notification')
        else:
            logger.info(reading.name + ' - No Notification Sent')
