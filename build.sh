#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run migrations (for SQLite)
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
