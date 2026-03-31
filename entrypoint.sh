#!/bin/sh

echo "Waiting for MySQL..."

while ! python -c "
import sys
import time
try:
    import MySQLdb
    MySQLdb.connect(host='db', port=3306, user='root', passwd='root2525', db='expense_tracker_db')
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