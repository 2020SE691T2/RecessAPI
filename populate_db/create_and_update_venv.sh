#!/bin/sh

venv_name="db_venv"
database_type="local"

# check if virtual environment already exists
if [ ! -d ${venv_name} ]; then
    # check version of python
    python_version="$(python -V 3>&1)"
    if [ "$(echo $python_version | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')" -lt "30" ]; then
        echo "This script requires python 3.0 or greater"
        return
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

python -m pip install --upgrade pip

# get /update requirements
pip install -r requirements.txt

# check if database is local only (default is Heroku)
if [[ ! -z $1 ]]; then
    database_type=$1
fi

# set vars
if [ ${database_type} == "Heroku" ]; then
    database_uri=$(awk -F "=" '/^database_heroku=/ {print $2}' envvars.txt)
else
    if [ ${database_type} == "local" ]; then
        database_uri=$(awk -F "=" '/^database_local=/ {print $2}' envvars.txt)
    else
        echo "unknown database host"
        return
    fi
fi

echo "Database: ${database_type}" 
echo "Database URI: ${database_uri}"

export database_uri
export database_type