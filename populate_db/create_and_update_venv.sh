#!/bin/sh

venv_name="db_venv"

# check if virtual environment already exists
if [ ! -d ${venv_name} ]; then
    # check version of python
    python_version="$(python -V 3>&1)"
    if [ "$(echo $python_version | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')" -lt "30" ]; then
        echo "This script requires python 3.0 or greater"
        exit 1
    fi
    
    # create the virtual environment
    echo "Creating virtual environment ${venv_name}"
    pip3 install virtualenv
    virtualenv -p /usr/bin/python3 ${venv_name}
else
    echo "${venv_name} already exists - update only"
fi

# activate the virtual environment
echo "Activating ${venv_name}"
activate() { . $PWD/${venv_name}/bin/activate; }
activate

python3 -m pip3 install --upgrade pip3

# get /update requirements
pip3 install -r requirements.txt

# set vars
database_uri=$(awk -F "=" '/^database_uri=/ {print $2}' envvars.txt)
export database_uri