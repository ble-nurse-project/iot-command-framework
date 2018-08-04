#!/bin/bash

hostnamectl set-hostname $1

systemctl enable ssh
systemctl start ssh

apt install python-pip -y
pip install paho-mqtt

./change_config.sh AGENT_OPTS=\"163.180.117.195 $1\"

cp agent.service /lib/systemd/system/agent.service

systemctl daemon-reload
systemctl enable agent

wget -qO- get.docker.com | sh
docker pull alicek106/ble-nurse-project:0.2

reboot
