#!/bin/sh
echo "Creating venv"

# Go to where the venv should be
cd ..

# Check if venv exits
if [ ! -d "venv/" ]; then
	echo "Creating virtual environment venv"

	# Create virtual environment
	python -m venv venv

 else
	echo "venv already exists - just going to update"
fi

echo "Entering venv first"
cd scripts/
source ./enter_venv.sh

# Get latest pip and requirements
cd ..
python -m pip install --upgrade pip
pip install -r requirements.txt

# set environment variables
database="Heroku"
# check if database is local only (default is Heroku)
if [[ ! -z $1 ]]; then
    database=$1
fi

if [ ${database} = "local" ]; then
    echo "Database: ${database}" 
    export DJANGO_SETTINGS_MODULE=RecessApplication.local_settings
fi

if [ ${database} = "Heroku" ]; then
    echo "Database: ${database}" 
    export DJANGO_SETTINGS_MODULE=RecessApplication.settings
fi
