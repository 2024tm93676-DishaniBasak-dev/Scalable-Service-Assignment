#!/bin/sh
set -e

# Wait and initialize DB
python /app/init_db.py

# Start gunicorn (exec to receive signals)
exec gunicorn --bind 0.0.0.0:5001 app:app