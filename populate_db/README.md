# Build Relational Database from CSV File w/ Python and Heroku

## Table of Contents
* [Schema](#schema)
* [Create Environment in Terminal to Build Database](#create-environment-in-terminal-to-build-database)
* [Generate Mock Data](#generate-mock-data)
* [Build Database and Populate Tables](#build-database-and-populate-tables)
* [Deactivate Database Build Environment](deactivate-database-build-environment)

## Schema
Schema is set in ```db_schema.py```

\[[toc](#table-of-contents)\]

## Create Environment in Terminal to Build Database
```console
// - Linux / macOS
source ./create_and_update_venv.sh <db_version>

// - Windows
./create_and_update_venv.sh <db_version>
```
\[[toc](#table-of-contents)\]

Where `<db_version>` is Heroku for the production database and local for the local database. Note that the script defaults to “local” if no `<db_version>` is provided.

## Generate Mock Data
```console
python gen_mock_data.py
```
\[[toc](#table-of-contents)\]

### Build Local Instance of POSTGRESQL Database

#### Setup (Only Needs to Be Done Once)
In the terminal, change the user to "postgres" with
```Console
sudo -i -u postgres
```
Create the database
```Console
createdb LocalRecessDB
```
Start the local database server
```Console
psql LocalRecessDB
```
Alter the user password
```
ALTER USER postgres WITH PASSWORD 'password';
```
**NOTE**: You should see "ALTER ROLE" if this was successful.
Exit
```
\q
```

In pgAdmin, Create a new Server.
* Under the General Tab, set Name to "LocalRecessDB"
* Under the Connection Tab, set the Host name/address to "localhost"
* Enter Password: "password"

\[[toc](#table-of-contents)\]


#### Build Local Instance

In the terminal, run
```console
source ./create_and_update_venv.sh local
```

**NOTE:** may require
```console
chmod u+x ./create_and_update_venv.sh
```
prior to running.

\[[toc](#table-of-contents)\]

### Build Heroku Database

In the terminal, run
```console
source ./create_and_update_venv.sh Heroku
```

**NOTE:** may require
```console
chmod u+x ./create_and_update_venv.sh
```
prior to running.

\[[toc](#table-of-contents)\]

## Build Database and Populate Tables
```console
source ./build_db.sh
```

**NOTE:** may require
```console
chmod u+x ./build_db.sh
```
prior to running.

\[[toc](#table-of-contents)\]

## Deactivate Database Build Environment
```console
deactivate
```
\[[toc](#table-of-contents)\]
