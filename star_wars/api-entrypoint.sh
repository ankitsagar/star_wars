#!/bin/bash

# Wait for the db
echo "Wait for the database to be available"
python manage.py wait_for_db

# Apply migrations
echo "Applying migrations"
python manage.py migrate

# populate data
echo "Populating data"
python manage.py load_data
python manage.py loaddata users

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
