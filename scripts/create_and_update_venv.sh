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