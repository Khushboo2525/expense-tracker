#!/bin/sh

echo "Waiting for MySQL..."

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_NAME="${DB_NAME:-expense_tracker_db}"

while ! python -c "
import sys
import os
try:
    import MySQLdb
    MySQLdb.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        passwd=os.environ.get('DB_PASSWORD', ''),
        db=os.environ.get('DB_NAME', 'expense_tracker_db'),
    )
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