#!/bin/sh

if [ "$1" = "celery" ]; then
    echo "Starting Celery worker..."
    exec "$@"
else
    echo "Running database migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Starting Gunicorn..."
    exec "$@"
fi