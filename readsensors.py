#!/usr/bin/env python3
from piot.service import SensorReadingSchedulingService

scheduling_service=SensorReadingSchedulingService()

scheduling_service.run_jobs()
