#!/bin/sh
set -x
export PYTHONPATH=/home/www/homeBakedPi/app:$PYTHONPATH
sudo /home/www/homeBakedPi/app/hbpApp.py /home/www/homeBakedPi/app/parameters.xml prod low
