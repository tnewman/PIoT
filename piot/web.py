""" PIoT Web Application Controllers
"""

from flask import Flask, render_template
import piot.service

app = Flask(__name__)

sensor_reading = piot.service.SensorReadingPersistenceService()


@app.route('/')
def show_sensor_readings():
    """ Show all recorded sensor readings.
    """

    readings = sensor_reading.all_reversed()

    return render_template('show_sensor_readings.html', readings=readings)
