#!/bin/sh

# Go to project root
cd $DOCKER_CONTAINER_SRC


if [ "$1" = "devserver" ]
then
    python manage.py migrate --noinput
    exec python manage.py runserver 0.0.0.0:8000
else
    service nginx start
    python manage.py migrate --noinput
    python manage.py collectstatic --no-input
    exec gunicorn -b 0.0.0.0:8000 -w $WORKERNUM -t 300 \
              --access-logfile - \
              --error-logfile - \
              async_service.wsgi:application
fi
