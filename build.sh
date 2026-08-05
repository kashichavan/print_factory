#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput

# Reset database schema and run migrations
python manage.py reset_db_schema || true
python manage.py migrate || true
python manage.py create_admin_user || true
