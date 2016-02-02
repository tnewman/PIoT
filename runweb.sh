#!/bin/bash
gunicorn piot.web:app --bind 0.0.0.0
