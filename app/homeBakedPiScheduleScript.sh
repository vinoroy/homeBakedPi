#!/bin/sh
set -x
export PYTHONPATH=/home/www/homeBakedPi:$PYTHONPATH
sudo /home/www/homeBakedPi/homeBakedPi.py /home/www/homeBakedPi/parameters.xml prod chkSchedules
