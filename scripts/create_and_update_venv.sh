#!/bin/sh
echo "Creating venv"

# Go to where the venv should be
cd ..

# Check if venv exits
if [ ! -d "venv/" ]; then
	echo "Creating virtual environment venv"

	# Create virtual environment
	python3 -m venv venv

 else
	echo "venv already exists - just going to update"
fi

echo "Entering venv first"

# Enter the virtual environment
activate() { . $PWD/venv/bin/activate; }
activate

# Get latest pip
python3 -m pip3 install --upgrade pip3

# Get latest requirements
pip3 install -r requirements.txt