class BaseSensor:
    def __init__(self):
        self.sensor_name = ''


class BaseAnalogSensor:
    def __init__(self):
        self.min_normal=None
        self.max_normal=None
        self.error_sentinel=None
    
    def read_analog_sensor(self):
        return None


class BaseDigitalSensor:
    def __init__(self):
        self.normal_value=False
    
    def read_digital_sensor(self):
        return None
