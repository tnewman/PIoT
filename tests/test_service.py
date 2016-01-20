from datetime import datetime
from piot.model import AnalogSensorReading
from piot.model import DigitalSensorReading
from piot.model import NotificationEvent
from piot.model import SensorReading
from piot.service import NotificationPersistenceService
from piot.service import SensorReadingPersistenceService
from piot.service import transaction_scope
from tests.fixtures import sqlalchemy


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
