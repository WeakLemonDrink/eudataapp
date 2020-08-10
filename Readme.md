# Tedearch web application

The Tedsearch web application provides a means to gather [TED](https://ted.europa.eu/TED/browse/browseByMap.do) data and analyse it. Evolution of the web application has lead to the development of a database of medicines based on the [British National Formulary (BNF)](https://bnf.nice.org.uk/), and pricing data for these medicines based on data available from [NHS Practice Level Prescribing](https://digital.nhs.uk/data-and-information/areas-of-interest/prescribing/practice-level-prescribing-in-england-a-summary) datasets provided via an API from [OpenPrescribing](https://openprescribing.net/). The latest version (v9.2) of the web application includes functionality to email notifications to users if search terms match recently gathered TED data.

A full description of the application is provided in `./doc/Tedsearch Description.docx`.

## Requirements
The web application was developed with [Python 3.7.2](https://www.python.org/downloads/release/python-372/) using [Django 2.2.2](https://docs.djangoproject.com/en/2.2/releases/2.2.2/).

Full requirements are provided in `requirements.txt`. The runtime provided in `Procfile` and `runtime.txt` is written to support the deployment of the application to the [Heroku](https://www.heroku.com/home) PaaS.

## The development environment
The development environment call be set up using a virtual environment set up using [virtualenv](https://virtualenv.pypa.io/en/stable/) and [pip](https://pypi.org/project/pip/). Once an environment has been set up, the `./scripts/dev_setup_env.sh` shell script can be used to load the environment to develop the project. The following environment variables are required:

* AWS_ACCESS_KEY_ID
* AWS_DEFAULT_REGION
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME
* DJANGO_SETTINGS_MODULE
* EMAIL_HOST_PASSWORD
* EMAIL_HOST_USER
* SECRET_KEY

The values for these variables are provided outside of this repository for security and should be copied to a `.env` file in the project root.

## The production environment
The project can be pushed to the Heroku production environment using the `./scripts/production_deploy.sh` shell script.
