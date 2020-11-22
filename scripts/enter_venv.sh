#!/bin/sh

os=$(./os.sh)

# Enter the virtual environment
if [[ $os -eq 3 ]]; then
	activate() { source ../venv/Scripts/Activate; }
else
	activate() { source ../venv/bin/activate; }
fi
activate