#!/bin/sh
sudo pkill gunicorn
sudo git pull
sudo /etc/init.d/nginx start
source ../env/bin/activate
sudo gunicorn app:app -b localhost:8000

