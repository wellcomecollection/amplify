# GCP

## About GCP

Google Cloud Platform (GCP) is a set of cloud computing services that run on the same infrastructure that Google uses internally for Google Search, Gmail, YouTube, etc. GCP includes APIs for Google's machine learning models.

The [Google Cloud Console](https://console.cloud.google.com) is a web UI used to provision, configure, manage, and monitor systems that use GCP.

## Create a project

To use services provided by GCP, you must create a project.

A project organizes all your GCP resources. A project consists of the following components:

- a set of collaborators
- enabled APIs (and other resources)
- monitoring tools
- billing information
- authentication and access controls

You can create multiple projects, but you'll only need one to run AMPLIFY.

In the Cloud Console, on the project selector page, create a Cloud project.

## Enable billing

A billing account defines who pays for a given set of resources. You configure billing when you create a project.

There's a generous free limit on the use of the APIs that AMPLIFY uses, but you'll still need to make sure that billing is enabled for the project in case you exceed that limit.

## Enable the APIs

AMPLIFY uses the Vision and Natural Language APIs, which need to be manually enabled.

[Enable the Vision API.](https://console.cloud.google.com/flows/enableapi?apiid=vision.googleapis.com)

[Enable the Natural Language API.](https://console.cloud.google.com/flows/enableapi?apiid=language.googleapis.com)

## Authentication

Set up authentication:

1. In the Cloud Console, go to the [**Create service account key**](https://console.cloud.google.com/apis/credentials/serviceaccountkey) page.
2. From the **Service account** list, select **New service account**.
3. In the **Service account name** field, enter a name.
4. From the **Role** list, select **Project > Owner**.
5. Click **Create**. A JSON file that contains your key downloads to your computer.

## Use the service account key file in your environment

Provide authentication credentials to the application code by setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable in the `.env` file at the root of this repo.
