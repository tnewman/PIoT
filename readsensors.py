#!/usr/bin/env python3

running = True

def signal_handler(signum, frame):
    global running
    running = False

# Signal handling must occur before SQLAlchemy imports 
# in the service layer, or the signal will not be 
# handled properly when the program first starts.
import signal
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

import schedule, time
from piot.service import SensorReadingSchedulingService

scheduling_service=SensorReadingSchedulingService()

def run_jobs():
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        while running:
            scheduling_service.sensor_reading_job()
            time.sleep(1)

if __name__ == '__main__':
    run_jobs()
