#!/usr/bin/env python3
import schedule, signal, time
from piot.service import SensorReadingSchedulingService

scheduling_service=SensorReadingSchedulingService()

running = True


def run_jobs():
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        schedule.every(30).seconds.do(scheduling_service.sensor_reading_job)
        scheduling_service.sensor_reading_job()

        while running:
            schedule.run_pending()
            time.sleep(1)


def signal_handler():
    global running
    running = False

if __name__ == '__main__':
    run_jobs()
