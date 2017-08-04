#!/bin/bash
apt-get update
apt-get install python-pika python-requests git python-dateutil curl python-pip
git clone https://github.com/amorrison9796/waggleWebAPI

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
dpkg-reconfigure locales

pip install --upgrade pip
pip install pytz
pip install flask

cp ./waggleWebAPI/send-node-metrics.service /etc/systemd/system
cp ./waggleWebAPI/start-web-app.service /etc/systemd/system

systemctl enable --now send-node-metrics.service
