# Build Relational Database from CSV File w/ Python and Heroku

## Table of Contents
* [Schema](#schema)
* [Generate Mock Data](#generate-mock-data)
* [Create Environment in Terminal to Build Database](#create-environment-in-terminal-to-build-database)
* [Build Database and Populate Tables](#build-database-and-populate-tables)
* [Deactivate Database Build Environment](deactivate-database-build-environment)

## Schema
Schema is set in ```db_schema.py```

## Generate Mock Data
```console
python3 gen_mock_data.py
```

## Create Environment in Terminal to Build Database
**The following variables will need to be set in the environment:**
```console
database_uri
```
Save these variables in a file ```envvars.txt``` in the same directory as ```create_and_update_venv.sh```, in the format:
```console
database_uri=<somestring>
```
**DO NOT USE " "**\
\
The appropriate values for database_url can be found by going to [Database Credentials: View Credentials...](https://data.heroku.com/datastores/016518f2-8a2b-4645-96e9-3ce4ef69f60d#administration) and copying URI.

In the terminal, run
```console
source ./create_and_update_venv.sh
```

**NOTE:** may require
```console
chmod u+x ./create_and_update_venv.sh
```
prior to running.

## Build Database and Populate Tables
```console
source ./build_db.sh
```

**NOTE:** may require
```console
chmod u+x ./build_db.sh
```
prior to running.

## Deactivate Database Build Environment
```console
deactivate
```

