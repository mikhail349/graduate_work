#!/bin/sh

[[ -z "$DB_HOST" ]] && { echo "Parameter DB_HOST is empty" ; exit 1; }
[[ -z "$DB_PORT" ]] && { echo "Parameter DB_PORT is empty" ; exit 1; }

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py collectstatic --noinput
celery -A config worker -B -D --loglevel=INFO
uwsgi --strict --ini config/uwsgi.ini