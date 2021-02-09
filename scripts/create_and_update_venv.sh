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

echo "Database: ${database}" 
if [ ${database} = "local" ]; then    
    export DBURL=$(awk -F "=" '/^database_local=/ {print $2}' envvars.txt)
fi

if [ ${database} = "Heroku" ]; then
    export DBURL=$(awk -F "=" '/^database_heroku=/ {print $2}' envvars.txt)
fi
export DJANGO_SETTINGS_MODULE=RecessApplication.settings

echo "Database URL: ${DBURL}"