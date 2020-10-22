#!/bin/sh

# Go to where the venv should be
cd ..

# Enter the virtual environment
source venv/Scripts/activate

# Enter backend code area
cd RecessApplication/

# Run tests
echo "Running tests"
python manage.py test

# Start the server
echo "Starting backend"
python manage.py runserver