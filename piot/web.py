""" PIoT Web Application Controllers
"""

from flask import Flask, render_template, request
import piot.service

app = Flask(__name__)

sensor_reading = piot.service.SensorReadingPersistenceService()


@app.route('/')
def show_sensor_readings():
    """ Show all recorded sensor readings.
    """

    page_number = request.args.get('page_number', default=0, type=int)
    page_size = request.args.get('page_size', default=100, type=int)

    paged_readings = sensor_reading.all_reversed(page_number, page_size)

    return render_template(
        'show_sensor_readings.html', paged_readings=paged_readings)
