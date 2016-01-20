from datetime import datetime
from piot.model import AnalogSensorReading
from piot.model import DigitalSensorReading
from piot.model import NotificationEvent
from piot.model import SensorReading
from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor
from piot.service import NotificationPersistenceService
from piot.service import SensorReadingPersistenceService
from piot.service import transaction_scope
from tests.fixtures import sensormodule, sqlalchemy
from tests import mocks
from unittest.mock import MagicMock


class TestBaseSQLAlchemyService:
    def test_all_returns_all_model_objects(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = AnalogSensorReading()
        service.create(reading)

        reading2 = AnalogSensorReading()
        service.create(reading2)

        assert len(service.all()) == 2

    def test_get_returns_single_model_object(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = AnalogSensorReading()
        service.create(reading)

        reading2 = AnalogSensorReading()
        service.create(reading2)

        assert service.get(reading.id).id == reading.id

    def test_update_updates_single_model_object(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        original_reading = AnalogSensorReading()
        original_reading.name = 'original'
        original_reading.value = 1
        original_reading.unit = 'original'

        service.create(original_reading)

        persisted_reading = service.get(original_reading.id)

        persisted_reading.name = 'new'
        persisted_reading.value = 2
        persisted_reading.unit = 'new'

        service.update(persisted_reading)

        updated_reading = service.get(original_reading.id)

        assert updated_reading.name == 'new'
        assert updated_reading.value == 2
        assert updated_reading.unit == 'new'

    def test_delete_deletes_single_model_object(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = AnalogSensorReading()
        service.create(reading)
        service.delete(reading)

        assert len(service.all()) == 0


class TestNotificationPersistenceService:
    def test_get_newest_notification(self):
        old_notification = NotificationEvent()
        old_notification.timestamp = datetime(2015, 1, 1)

        new_notification = NotificationEvent()
        new_notification.timestamp = datetime(2016, 1, 1)

        service = NotificationPersistenceService()

        # Insert in reverse order to confirm order by
        service.create(new_notification)
        service.create(old_notification)

        assert service.get_newest_notification().timestamp == \
               new_notification.timestamp


class TestSensorReadingPersistenceService:
    def test_sensor_reading(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = SensorReading()
        service.create(reading)

        assert service.get(reading.id).id == reading.id

    def test_analog_sensor_reading(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = AnalogSensorReading()
        service.create(reading)

        assert service.get(reading.id).id == reading.id

    def test_digital_sensor_reading(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = DigitalSensorReading()
        service.create(reading)

        assert service.get(reading.id).id == reading.id

    def test_polymorphic(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        reading = SensorReading()
        analog = AnalogSensorReading()
        digital = DigitalSensorReading()

        service.create(reading)
        service.create(analog)
        service.create(digital)

        assert len(service.all()) == 3


class TestSensorReadingSchedulingService:
    def test_sensor_reading_job_analog_below_normal(self, sensormodule,
                                                    sqlalchemy):
        sensormodule.sensor.sensors = [mocks.MockAnalogBelowNormalSensor]

        sensormodule._sensor_reading_job()

        sensor_persistence = SensorReadingPersistenceService()
        sensor = sensor_persistence.all()[0]

        assert sensor.name == 'analog below normal'
        assert sensor.value == 0
        assert sensor.unit == 'below normal analog unit'

    def test_sensor_reading_job_analog_normal(self, sensormodule, sqlalchemy):
        sensormodule.sensor.sensors = [mocks.MockAnalogNormalSensor]

        sensormodule._sensor_reading_job()

        sensor_persistence = SensorReadingPersistenceService()
        sensor = sensor_persistence.all()[0]

        assert sensor.name == 'analog normal'
        assert sensor.value == 1
        assert sensor.unit == 'normal analog unit'

    def test_sensor_reading_job_analog_above_normal(self, sensormodule,
                                                    sqlalchemy):
        sensormodule.sensor.sensors = [mocks.MockAnalogAboveNormalSensor]

        sensormodule._sensor_reading_job()

        sensor_persistence = SensorReadingPersistenceService()
        sensor = sensor_persistence.all()[0]

        assert sensor.name == 'analog above normal'
        assert sensor.value == 2
        assert sensor.unit == 'above normal analog unit'

    def test_sensor_reading_job_analog_sentinel(self, sensormodule, sqlalchemy):
        sensormodule.sensor.sensors = [mocks.MockAnalogSentinelSensor]

        sensormodule._sensor_reading_job()

        sensor_persistence = SensorReadingPersistenceService()
        sensor = sensor_persistence.all()[0]

        assert sensor.name == 'analog sentinel'
        assert sensor.value == 3
        assert sensor.unit == 'analog sentinel unit'

    def test_sensor_reading_job_digital_normal(self, sensormodule,
                                               sqlalchemy):
        sensormodule.sensor.sensors = [mocks.MockDigitalNormalSensor]

        sensormodule._sensor_reading_job()

        sensor_persistence = SensorReadingPersistenceService()
        sensor = sensor_persistence.all()[0]

        assert sensor.name == 'digital normal'
        assert sensor.value is False

    def test_sensor_reading_job_digital_abnormal(self, sensormodule,
                                                 sqlalchemy):
        sensormodule.sensor.sensors = [mocks.MockDigitalAbnormalSensor]

        sensormodule._sensor_reading_job()

        sensor_persistence = SensorReadingPersistenceService()
        sensor = sensor_persistence.all()[0]

        assert sensor.name == 'digital abnormal'
        assert sensor.value is True


class TestTransactionScope:
    def test_rollback(self, sqlalchemy):
        try:
            with transaction_scope() as session:
                reading = SensorReading()
                session.add(reading)

                raise ValueError('Test Transactions!')
        except ValueError:
            pass

        service = SensorReadingPersistenceService()
        assert len(service.all()) == 0
