#!/bin/sh

source ./enter_venv.sh

cd ..

# Logs directory must be created manually
if [ ! -d "logs/" ]; then
	mkdir logs
fi
# Clean out all old logs
rm logs/*

# Start the server
echo "Starting backend"
python manage.py runserver