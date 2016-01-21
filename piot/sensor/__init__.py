from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor, BaseSensor
import importlib
import pkgutil
import os

plugin_directory=os.path.dirname(__file__)


class SensorClasses:
    def get_all_sensor_classes(self):
        return self.get_analog_sensor_classes() + \
            self.get_digital_sensor_classes()

    def get_analog_sensor_classes(self):
        self._load_all_package_modules()
        return BaseAnalogSensor.__subclasses__()

    def get_digital_sensor_classes(self):
        self._load_all_package_modules()
        return BaseDigitalSensor.__subclasses__()

    def _load_all_package_modules(self):
        for module in pkgutil.iter_modules([plugin_directory]):
            name_index = 1
            importlib.import_module('.' + module[name_index], __package__)
