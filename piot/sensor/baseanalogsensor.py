class BaseAnalogSensor:
    def __init__(self):
        self.min_in_range=None
        self.max_in_range=None
        self.error_flag=None
    
    def read_analog_sensor(self):
        return None