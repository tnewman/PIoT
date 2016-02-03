""" Provides access to all analog and digital sensors in the PIoT sensor
    plugin folder. Sensors simply need to inherit one of the base sensor
    classes and exist in the sensor folder to be detected by the sensor
    reading job.
"""

from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor, BaseSensor
import importlib
import pkgutil
import os

plugin_directory=os.path.dirname(__file__)


class SensorClasses:
    """ Allows access to all Sensor classes.
    """

    def get_all_sensor_classes(self):
        """ Retrieve all sensor classes (analog and digital) from the PIoT
            sensor plugin folder.
        :return: All sensor classes in the sensor plugin folder.
        :rtype: List of BaseSensor classes.
        """

        return self.get_analog_sensor_classes() + \
            self.get_digital_sensor_classes()

    def get_analog_sensor_classes(self):
        """ Retrieves all analog sensor classes from the PIoT sensor plugin
            folder.
        :return: All analog sensor classes in the sensor plugin folder.
        :rtype: List of BaseAnalogSensor classes.
        """

        self._load_all_package_modules()
        return BaseAnalogSensor.__subclasses__()

    def get_digital_sensor_classes(self):
        """ Retrieves all digital sensor classes from the PIoT sensor plugin
            folder.
        :return: All sensor classes in the sensor plugin folder.
        :rtype: List of BaseDigitalSensor classes.
        """

        self._load_all_package_modules()
        return BaseDigitalSensor.__subclasses__()

    def _load_all_package_modules(self):
        for module in pkgutil.iter_modules([plugin_directory]):
            name_index = 1
            importlib.import_module('.' + module[name_index], __package__)
