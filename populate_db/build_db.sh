#!/bin/sh

venv_name="db_venv"

if [ -d ${venv_name} ]; then
    # activate the virtual environment
    echo "Activating ${venv_name}"
    activate() { . $PWD/${venv_name}/bin/activate; }
    activate
    
    echo "Building database"
    python main.py
else
    echo "virtual environment does not exist"
    echo "run create_and_update_venv.sh first"
fi