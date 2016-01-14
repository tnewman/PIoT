#!/usr/bin/env python3
import sys
sys.path.append("..")

from piot.sensor.sumppump import SumpPump

print('Sump Pump Sensor Test Script')
print('Place an object 30cm away from sensor and press enter')
input()

sump_pump=SumpPump()
distance=sump_pump.read_analog_sensor()

if(distance>=30-2 or distance<=30+2):
    print('Test Passed')
    exit(0)
else:
    print('Test Failed')
    exit(1)