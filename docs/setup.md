# Setup instructions

## Running

Amplify is orchestrated with [docker](https://www.docker.com/products/docker-desktop).

To set up the project locally, run `docker-compose build` to build the necessary images, and `docker-compose up` to run them together.

This will create a [Flask](https://flask.palletsprojects.com/en/1.1.x/) API which retrieves and parses data from the third party machine learning and catalogue APIs, and an [Angular](https://angular.io/) front-end which allows librarians to interact with the system.

## Obtaining credentials

Credentials required for this project are stored in a local `.env` file.

The variables listed in `.env` are read by the `docker-compose up` command, and are passed into the appropriate images as environment variables.

This repo comes with a `blank.env` file - you should rename this as `.env` and fill in the appropriate values according to the instructions below.

### Google Cloud ML

Amplify uses Google's machine learning APIs for text recognition, translation, and entity recognition.

You'll need to obtain a set of credentials from google to use these APIs. See instructions [here](https://cloud.google.com/vision/docs/setup). You'll need to authorise that set of credentials to use the Vision and Natural Language APIs.

### Worldcat

The worldcat API requires a key. Obtain this by... TODO
