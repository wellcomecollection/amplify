# Setup instructions

## Running

Amplify is orchestrated with [docker](https://www.docker.com/products/docker-desktop).

To set up the project locally, run `docker-compose up --build`. This will build and run the necessary images.

This will create a [Flask](https://flask.palletsprojects.com/en/1.1.x/) API which retrieves and parses data from the third party machine learning and catalogue APIs, and an [Angular](https://angular.io/) front-end which allows librarians to interact with the system. The interface should be available at `localhost:90`

## Obtaining credentials

Credentials required for this project are stored in a local `.env` file.

The variables listed in `.env` are read by the `docker-compose up` command, and are passed into the appropriate images as environment variables.

This repo comes with a `blank.env` file - you should rename this as `.env` and fill in the appropriate values according to the instructions below.

### Google Cloud ML

Amplify uses Googles machine learning APIs for OCR, translation, and entity recognition. See the instructions [here](gcp.md) for setting up the Google Cloud Platform for AMPLIFY.
