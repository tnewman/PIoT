import re
from datetime import datetime
from piot import web
from piot.model import AnalogSensorReading, DigitalSensorReading
from piot.service import SensorReadingPersistenceService
from tests.fixtures import sensormodule, sqlalchemy

class TestWeb:
    def test_index_analog_sensor_reading(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        timestamp = datetime.now()

        reading = AnalogSensorReading()
        reading.name = 'testsensor'
        reading.unit = 'testunit'
        reading.value = 0
        reading.timestamp = timestamp

        service.create(reading)

        client = web.app.test_client()

        rv = client.get('/')

        assert b'testsensor' in rv.data
        assert b'Analog' in rv.data
        assert b'0 (testunit)' in rv.data
        assert str.encode(str(timestamp)) in rv.data
        assert b'newer' not in rv.data
        assert b'older' not in rv.data

    def test_index_digital_sensor_reading(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        timestamp = datetime.now()

        reading = DigitalSensorReading()
        reading.name = 'testsensor'
        reading.value = True
        reading.timestamp = timestamp

        service.create(reading)

        client = web.app.test_client()

        rv = client.get('/')

        assert b'testsensor' in rv.data
        assert b'Digital' in rv.data
        assert b'True' in rv.data
        assert str.encode(str(timestamp)) in rv.data

    def test_index_timestamp_reverse_order(self, sqlalchemy):
        service = SensorReadingPersistenceService()

        old = DigitalSensorReading()
        old.name = 'testsensor'
        old.value = True
        old.timestamp = datetime.now()

        new = DigitalSensorReading()
        new.name = 'testsensor'
        new.value = True
        new.timestamp = datetime.now()

        service.create(old)
        service.create(new)

        client = web.app.test_client()

        rv = client.get('/')

        rv_str = rv.data.decode('utf-8')

        matches = re.findall('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\.\d\d\d\d\d\d',
                             rv_str)

        assert matches[0] == str(new.timestamp)
        assert matches[1] == str(old.timestamp)
