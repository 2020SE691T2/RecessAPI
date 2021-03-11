# Recess API
## Code Quality Metrics
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=bugs)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=code_smells)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=ncloc)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=security_rating)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=sqale_index)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=2020SE691T2_RecessAPI&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=2020SE691T2_RecessAPI)

## Overview

This project was started and completed to its current state as part of degree requirements for the MS Software Engineering degree from Drexel University. This project was completed in the SE691 course which covers two terms and lasts approximately six months.

The goal of the project was to create a remote learning tool with class management with a focus on early education and younger children. The application is intentionally minimalistic in features and uses a colorful design in order to appeal to that target audience without overcomplicating the root of what needs to get done: get children to their virtual classroom.

This README describes the API that connects our website to our data. To learn more about the site and web app itself, please see this repo: https://github.com/2020SE691T2/RecessApplication

## Table of Contents
* [Overview](#overview)
* [Installation and Starting](#installation-and-starting)
* [3rd Party Technologies Used](#3rd-party-technologies-used)
* [Build and Populate Database](#build-and-populate-database)
* [Build Environment and Run the Application](#build-environment-and-run-the-application)
* [Next Steps & Outstanding Work Items](#next-steps-&-outstanding-work-items)

## Installation and Starting
Fork or download this repo to your local machine.

\[[toc](#table-of-contents)\]

## 3rd Party Technologies Used
* Python 3.7
* Pip 3.7
* Django
* PostgreSQL
* Mailgun
* Zoom

\[[toc](#table-of-contents)\]

## Build and Populate Database
See  [Populate DB README](https://github.com/2020SE691T2/RecessAPI/blob/main/populate_db/README.md). 

\[[toc](#table-of-contents)\]
## Build Environment and Run the Application
### Build the virtual environment
cd into `scripts` directory.
```
// - Linux / macOS
source ./create_and_update_venv.sh <db_version>

// - Windows
./create_and_update_venv.sh <db_version>
```
Where `<db_version>` is Heroku for the production database and local for the local database. Note that the script defaults to “Heroku” if no `<db_version>` is provided.

This will install all dependencies in the `requirements.txt` in the parent directory. It will also enter the virtual environment and `cd` up to the parent directory.

\[[toc](#table-of-contents)\]

### Run the server locally

To run the server, in the parent directory containing `manage.py`
```
python manage.py runserver
```
\[[toc](#table-of-contents)\]

## Next Steps & Outstanding Work Items
Items yet to be completed for the project can be found on this repo’s issue board here: https://github.com/2020SE691T2/RecessAPI/issues.

Other general recommendations on how to take this project to the next level might include:
* Gradebook
* Messaging
* In-application video chat support instead of relying on Zoom
* Assignment Management

#### Original Contributors
https://github.com/gateship1 \
https://github.com/jonathanmcdaniel \
https://github.com/DylanZeller \
https://github.com/msknobloch2 \
https://github.com/coxwm11 \
https://github.com/jdurelli \

\[[toc](#table-of-contents)\]