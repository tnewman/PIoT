""" PIoT Services
"""

from contextlib import contextmanager
from datetime import datetime, timedelta

import logging
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from piot import config
from piot.sensor import SensorClasses
from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor
from piot.model import NotificationEvent, AnalogSensorReading, \
    DigitalSensorReading, PagedResult, SensorReading
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
        :rtype: list of piot.model.Base
        """

        with transaction_scope() as session:
            records = session.query(self._model).with_polymorphic('*').all()

        return records

    def get(self, key):
        """ Retrieves a specific record.
        :param key: Primary Key of record to retrieve.
        :type key: int
        :return: Record specified by the id.
        :rtype model: piot.model.Base
        """

        with transaction_scope() as session:
            record = session.query(self._model).with_polymorphic('*') \
                .filter_by(id=key).first()

        return record

    def create(self, object):
        """ Creates a new record.
        :param object: The new record.
        :type object: piot.model.Base
        """

        with transaction_scope() as session:
            session.add(object)

    def update(self, object):
        """ Updates an existing record.
        :param object: The existing record.
        :type object: piot.model.Base
        """

        with transaction_scope() as session:
            session.merge(object)
    
    def delete(self, object):
        """ Deletes an existing record.
        :param object: The existing record.
        :type object: piot.model.Base
        """

        with transaction_scope() as session:
            session.delete(object)


class NotificationPersistenceService(BaseSQLAlchemyService):
    def __init__(self):
        """ Provides database CRUD operations for Notifications.
        """

        super().__init__(NotificationEvent)

    def get_newest_notification(self, sensor_name):
        """ Retrieves the newest notification based on timestamp.
        :param sensor_name: The name of the sensor to retrieve the newest
                            notification for.
        :type sensor_name: str
        :return: Newest Notification
        :rtype: NotificationEvent
        """

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
        """ Provides database CRUD operations for Sensor Readings.
        """

        super().__init__(SensorReading)

    def all_reversed(self, page_number, page_size):
        """ Reads all sensor readings in reverse order by timestamp.
        :param page_number: The number of the record page to retrieve.
        :type page_number: int
        :param page_size: The size of each record page.
        :type page_size: int
        :return: Paged sensor readings in reverse order by timestamp.
        :rtype: piot.model.Paged
        """

        with transaction_scope() as session:
            query = session.query(SensorReading).with_polymorphic('*')\
                .order_by(desc(SensorReading.timestamp))

            count = query.count()
            readings = query.limit(page_size).offset(page_number).all()

            page = PagedResult()
            page.total_pages = int(count / page_size + 1)
            page.page_number = page_number
            page.page_size = page_size

            if page.page_number > page.total_pages or page.page_number < 0:
                page.elements = []
            else:
                page.elements = readings

        return page


class SensorReadingSchedulingService:
    def __init__(self, sensor_class=SensorClasses,
                 sms_notification=TwilioSMSNotification):
        """ Reads all sensors in the sensor plugin folder, logs the values
            read from the sensors and sends notifications for abnormal sensor
            values.
        :param sensor_class: Provides access to all sensor classes.
        :type sensor_class: SensorClasses class
        :param sms_notification: Notification class to use for SMS
                                 notifications.
        :type sms_notification: Notification class
        """

        self.sensor_class = sensor_class()
        self.sensor_persistence = SensorReadingPersistenceService()
        self.notification_persistence = NotificationPersistenceService()
        self.sms_notification = sms_notification()

    def sensor_reading_job(self):
        """ Reads all sensors in the plugin folder, logs the values read from
            the sensors and sends notifications for abnormal sensor values.
        """

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
