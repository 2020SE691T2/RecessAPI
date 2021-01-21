#!/bin/sh

source ./enter_venv.sh

cd ..

# Tests require the log directory too
if [ ! -d "logs/" ]; then
	mkdir logs
fi

pytest --cov-report xml:coverage-reports/coverage.xml --cov=RecessApplication -s