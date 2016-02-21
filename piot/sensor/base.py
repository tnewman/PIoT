""" Base Classes for PIoT Sensors
"""


class BaseSensor:
    def __init__(self):
        """ Base Sensor
        """

        self.sensor_name = ''
        """The name of the sensor. """

    def get_notification_text(self, sensor_value):
        """ Get the notification text for the sensor.
        :param sensor_value: The sensor value to send in the notification.
        :type sensor_value: float for Analog Sensors/bool for Digital
                            Sensors
        :return:
        """
        return ''


class BaseAnalogSensor(BaseSensor):
    def __init__(self):
        """ Base Analog Sensor
        """

        self.min_normal = 0
        """ The minimum acceptable sensor value. Values below this are
            considered abnormal and will trigger notifications. """

        self.max_normal = 0
        """ The maximum acceptable sensor value. Values above this are
            considered to be abnormal and will trigger notifications. """

        self.error_sentinel = None
        """ A sensor reading that matches the error sentinel will be
            considered a bad reading and will be ignored. """

        self.unit = ''
        """ The unit of the sensor reading (cm, mm, etc.). """

    def read_analog_sensor(self):
        """ Reads a value from the sensor.
            :return: Value read from the sensor.
            :rtype: int or float
        """

        return None


class BaseDigitalSensor(BaseSensor):
    def __init__(self):
        """ BaseDigitalSensor
        """

        self.normal_value = False
        """ The value is considered normal. The inverse of this value will
            trigger notifications. """

    def read_digital_sensor(self):
        """ Reads a value from the sensor.
            :return: Value read from the sensor.
            :rtype: True or False
        """

        return None
