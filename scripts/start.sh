#!/bin/sh

# Go to where the venv should be
cd ..

# Enter the virtual environment
activate() { . $PWD/venv/bin/activate; }
activate

# Enter backend code area
#cd RecessApplication/

# Run tests
#echo "Running tests"
#python3 manage.py test

# Start the server
echo "Starting backend"
python3 manage.py runserver