class BaseSensor:
    def __init__(self):
        self.sensor_name = ''
        self.notification_text = ''


class BaseAnalogSensor(BaseSensor):
    def __init__(self):
        self.min_normal = 0
        self.max_normal = 0
        self.error_sentinel = None
        self.unit = ''

    def read_analog_sensor(self):
        return None


class BaseDigitalSensor(BaseSensor):
    def __init__(self):
        self.normal_value = False
    
    def read_digital_sensor(self):
        return None
