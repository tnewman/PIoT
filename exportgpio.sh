#!/bin/bash

if [ -d /sys/class/gpio/gpio23 ]; then
    echo "GPIO 23 is already exported"
else
    echo "Exporting GPIO 23"
    echo 23 > /sys/class/gpio/export
fi

if [ -d /sys/class/gpio/gpio24 ]; then
    echo "GPIO 24 is already exported"
else
    echo "Exporting GPIO 24"
    echo 24 > /sys/class/gpio/export
fi
