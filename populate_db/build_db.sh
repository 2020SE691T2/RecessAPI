#!/bin/sh

venv_name="db_venv"

# activate the virtual environment
echo "Activating ${venv_name}"
. ${venv_name}/bin/activate

echo "Building database"
python main.py