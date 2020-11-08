#!/bin/sh

source ./enter_venv.sh

cd ..

pytest --cov-report xml:coverage-reports/coverage.xml --cov=RecessApplication