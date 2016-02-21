import time
from periphery import GPIO
from piot.sensor.base import BaseAnalogSensor


class SumpPump(BaseAnalogSensor):
    def __init__(self):
        """ Sump Pump Sensor
        """

        self.sensor_name = 'Sump Pump Monitor'
        self.min_normal = 30
        self.max_normal = 10000
        self.unit = 'cm'
        self.error_sentinel = None

    def get_notification_text(self, sensor_value):
        return 'Sump Pump Monitor - High Water Level - (' + \
               str(sensor_value) + ' ' + self.unit + \
               ') Please check the sump pump.'

    def read_analog_sensor(self):
        """ Reads the Sump Pump sensor.
        :return: Distance to Sump Pump water.
        :rtype: float
        """

        trig=GPIO(23, 'out')
        echo=GPIO(24, 'in')

        # Pulse to trigger sensor
        trig.write(False)
        time.sleep(0.00001)
        trig.write(True)
        time.sleep(0.00001)
        trig.write(False)

        while echo.read()==False:
            pulse_start=time.time()

        while echo.read()==True:
            pulse_end= time.time()

        pulse_duration=pulse_end-pulse_start

        # Quick explaination of the formula:
        # The pulse duration is to the object and back, so the 
        # distance is one half of the pulse duration. The speed of 
        # sound in air is 340 meters/second. There are 100 centimeters 
        # in a meter.
        distance=pulse_duration*340/2*100
        distance=round(distance, 2)

        trig.close()
        echo.close()

        return distance
