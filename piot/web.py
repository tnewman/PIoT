from flask import Flask, render_template
import piot.service

app = Flask(__name__)

sensor_reading = piot.service.SensorReadingPersistenceService()


@app.route('/')
def show_sensor_readings():
    readings = sensor_reading.all()

    return render_template('show_sensor_readings.html', readings=readings)
