from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor

class MockAnalogBelowNormalSensor(BaseAnalogSensor):
    def __init__(self):
        self.sensor_name = 'analog below normal'
        self.min_normal = 1
        self.max_normal = 2
        self.error_sentinel= 3
        self.unit = 'below normal analog unit'

    def get_notification_text(self, sensor_value):
        return'analog below normal notification'

    def read_analog_sensor(self):
        return 0


class MockAnalogNormalSensor(BaseAnalogSensor):
    def __init__(self):
        self.sensor_name = 'analog normal'
        self.min_normal = 0
        self.max_normal = 2
        self.error_sentinel= 3
        self.unit = 'normal analog unit'

    def get_notification_text(self, sensor_value):
        return 'analog normal notification'

    def read_analog_sensor(self):
        return 1


class MockAnalogAboveNormalSensor(BaseAnalogSensor):
    def __init__(self):
        self.sensor_name = 'analog above normal'
        self.min_normal = 0
        self.max_normal = 1
        self.error_sentinel= 3
        self.unit = 'above normal analog unit'

    def get_notification_text(self, sensor_value):
        return 'analog above normal notification'

    def read_analog_sensor(self):
        return 2


class MockAnalogSentinelSensor(BaseAnalogSensor):
    def __init__(self):
        self.sensor_name = 'analog sentinel'
        self.min_normal = 0
        self.max_normal = 1
        self.error_sentinel = 3
        self.unit = 'analog sentinel unit'

    def get_notification_text(self, sensor_value):
        return'analog sentinel notification'

    def read_analog_sensor(self):
        return 3


class MockDigitalNormalSensor(BaseDigitalSensor):
    def __init__(self):
        self.sensor_name = 'digital normal'
        self.normal_value = False

    def get_notification_text(self, sensor_value):
        return'digital normal notification'

    def read_digital_sensor(self):
        return False


class MockDigitalAbnormalSensor(BaseDigitalSensor):
    def __init__(self):
        self.sensor_name = 'digital abnormal'
        self.normal_value = False

    def get_notification_text(self, sensor_value):
        return 'digital abnormal notification'

    def read_digital_sensor(self):
        return True
