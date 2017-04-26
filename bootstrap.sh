#!/usr/bin/env bash 
apt-get update -y
apt-get -y install python3.4-dev libffi-dev python3-pip python3.4-venv 
wget https://raw.githubusercontent.com/ciarancoffey/yacmt/master/requirements.txt -O /root/requirements.txt
python3 -m venv /root/yacmt
. /root/yacmt/bin/activate
pip install -r /root/requirements.txt
deactive
