#!/bin/bash

# Wait for the db
echo "Wait for the database to be available"
python star_wars/manage.py wait_for_db

# Apply migrations
echo "Applying migrations"
python star_wars/manage.py migrate

# populate data
echo "Populating data"
python star_wars/manage.py load_data
python star_wars/manage.py loaddata users

# Start server
echo "Starting server"
python star_wars/manage.py runserver 0.0.0.0:8000
