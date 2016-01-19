from contextlib import contextmanager

import schedule, time
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from piot import config, sensor
from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor
from piot.model import NotificationEvent, AnalogSensorReading, DigitalSensorReading, SensorReading
from piot.notification import TwilioSMSNotification

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

    def get_newest_notification(self):
        with transaction_scope() as session:
            record = session.query(self._model).order_by(
                    desc(self._model.timestamp)).first()

        return record


class SensorReadingPersistenceService(BaseSQLAlchemyService):
    def __init__(self):
        super().__init__(SensorReading)


class SensorReadingSchedulingService:
    def __init__(self, schedule=schedule, sensor=sensor,
                 sms_notification=TwilioSMSNotification, time=time):
        self.schedule = schedule
        self.sensor = sensor
        self.sensor_persistence = SensorReadingPersistenceService()
        self.notification_persistence = NotificationPersistenceService()
        self.sms_notification = sms_notification
        self.run_continuously = True
        self.time = time

    def run_jobs(self):
        self.scheduler.every(30).seconds.do(self._sensor_reading_job)
        self._sensor_reading_job()

        while self.run_continuously:
            self.scheduler.run_pending()
            time.sleep(1)

    def _sensor_reading_job(self):
        for sensor_class in sensor.get_all_sensor_classes():
            if sensor_class is BaseAnalogSensor:
                self._read_analog_sensor(sensor_class())
            elif sensor_class is BaseDigitalSensor:
                self._read_digital_sensor(sensor_class())
            else:
                # Not sure what to do in the default case
                pass

    def _read_analog_sensor(self, analog_sensor):
        value = analog_sensor.read_analog_sensor()

        if value != analog_sensor.error_sentinel:
            if value < analog_sensor.min_normal or \
                    value > analog_sensor.max_normal:
                self._send_notification(analog_sensor)

        analog_reading = AnalogSensorReading()
        analog_reading.name = analog_sensor.sensor_name
        analog_reading.value = value
        analog_reading.unit = analog_sensor.unit
        self.sensor_persistence.create(analog_reading)

    def _read_digital_sensor(self, digital_sensor):
        value = digital_sensor.read_digital_sensor()

        if value != digital_sensor.normal_value:
            self._send_notification(digital_sensor)

        digital_reading = DigitalSensorReading()
        digital_reading.name = digital_sensor.sensor_name
        digital_sensor.value = value
        self.sensor_persistence.create(digital_sensor)

    def _send_notification(self, notification_sensor, reading):
        self.sms_notification.send_notification(
                notification_sensor.notification_text)

        notification_event = NotificationEvent()
        notification_event.sensor_id = reading.id
        self.notification_persistence.create(notification_event)
