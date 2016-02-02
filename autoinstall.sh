#!/bin/bash

echo "PI of Things (PIoT) Auto-Installer"

if [ $(whoami) != "root" ]; then
    echo "Script must be run as root! Exiting."
    exit 1
fi

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install git python3-pip

git clone https://github.com/tnewman/piot /home/pi/PIoT

chown -R pi /home/pi/PIoT
chgrp -R pi /home/pi/PIoT

cd /home/pi/PIoT

python3 setup.py develop

pip3 install gunicorn

cp config.cfg.sample config.cfg

./initializedatabase.py

cp piotexportgpio.service /etc/systemd/system/piotexportgpio.service
cp piotreadsensors.service /etc/systemd/system/piotreadsensors.service
cp piotweb.service /etc/systemd/system/piotweb.service

systemctl daemon-reload

systemctl enable piotexportgpio.service
systemctl enable piotreadsensors.service
systemctl enable piotweb.service

systemctl restart piotexportgpio.service
systemctl restart piotreadsensors.service
systemctl restart piotweb.service

echo "PIoT Successfully Installed!"
