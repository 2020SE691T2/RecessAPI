#!/bin/sh

source ./enter_venv.sh

cd ..

# Start the server
echo "Starting backend"
python manage.py runserver