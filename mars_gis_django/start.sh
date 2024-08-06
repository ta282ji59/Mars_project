#!/bin/bash

sleep 5
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
# ここで読込
# uwsgi --ini /server/config/uwsgi.ini
uwsgi --socket :8001 --module mars_gis_django.wsgi