from piot.sensor.base import BaseAnalogSensor, BaseDigitalSensor, BaseSensor
import importlib
import pkgutil
import os

plugin_directory=os.path.dirname(__file__)


def load_all_package_modules():
    for module in pkgutil.iter_modules([plugin_directory]):
        name_index = 1
        importlib.import_module('.' + module[name_index], __package__)


def get_all_sensor_classes():
    return get_analog_sensor_classes() + \
        get_digital_sensor_classes()


def get_analog_sensor_classes():
    load_all_package_modules()
    return BaseAnalogSensor.__subclasses__()


def get_digital_sensor_classes():
    load_all_package_modules()
    return BaseDigitalSensor.__subclasses__()
