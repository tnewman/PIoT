import piot.service
import pytest
from piot.notification import TwilioSMSNotification
from piot.model import Base
from piot.sensor import BaseAnalogSensor, BaseDigitalSensor
from piot.service import SensorReadingSchedulingService
from sqlalchemy import create_engine
from unittest.mock import MagicMock

sqlalchemyengine = create_engine('sqlite:///:memory:')


@pytest.fixture()
def sqlalchemy():
    # SQLAlchemy recommends a single engine is used across an application
    piot.service.engine = sqlalchemyengine

    Base.metadata.drop_all(bind=sqlalchemyengine)
    Base.metadata.create_all(bind=sqlalchemyengine)


class MockSensor:
    def __init__(self):
        self.sensors = []

    def get_all_sensor_classes(self):
        return self.sensors


@pytest.fixture()
def sensormodule():
    sms_notification = TwilioSMSNotification()

    sensor_service = SensorReadingSchedulingService(sensor_class=MockSensor)
    sensor_service.sms_notification.send_notification = MagicMock()
    return sensor_service
