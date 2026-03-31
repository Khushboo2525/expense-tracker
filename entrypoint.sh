#!/bin/sh

echo "Waiting for MySQL..."

while ! python -c "
import sys
try:
    import MySQLdb
    MySQLdb.connect(host='$DB_HOST', port=int('$DB_PORT'), user='$DB_USER', passwd='$DB_PASSWORD', db='$DB_NAME')
    sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(1)
" ; do
    echo "MySQL not ready, retrying in 3 seconds..."
    sleep 3
done

echo "MySQL is ready!"
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn expense_tracker.wsgi:application --bind 0.0.0.0:8000