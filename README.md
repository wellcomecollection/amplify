# AMPLIFY
Assisted Metadata Processing for Libraries – a Feasibility Study

## Requirements:
You will need to get access to the Google Cloud Platform (GCP) resources used in this project. Please request access from the project owner or follow instructions here for creating a new GCP and service account: https://cloud.google.com/vision/docs/setup

After creating the account download and update the path to your credentials and config.py GOOGLE_APPLICATION_CREDENTIALS_PATH.

### About the GCP Console

The [Google Cloud Console](https://console.cloud.google.com/?_ga=2.117001414.1169747201.1592461708-1311944522.1592461708) is a web UI used to provision, configure, manage, and monitor systems that use GCP products. You use the Cloud Console to set up and manage Vision resources.

### Create a project
To use services provided by GCP, you must create a project.

A project organizes all your GCP resources. A project consists of the following components:

* a set of collaborators
* enabled APIs (and other resources)
* monitoring tools
* billing information
* authentication and access controls

You can create one project, or you can create multiple projects. You can use your projects to organize your GCP resources in a resource hierarchy. For more information on projects, see the Resource Manager documentation.

In the Cloud Console, on the project selector page, select or create a Cloud project.

### Enable billing

A billing account defines who pays for a given set of resources. Billing accounts can be linked to one or more projects. Project usage is charged to the linked billing account. You configure billing when you create a project. For more information, see the Billing documentation.

Make sure that billing is enabled for your Google Cloud project. Learn how to confirm billing is enabled for your project.

### Enable the API

You must enable the Vision API for your project. For more information on enabling APIs, see the Service Usage documentation.

[Enable the Vision API.](https://console.cloud.google.com/flows/enableapi?apiid=vision.googleapis.com&_ga=2.143320181.1169747201.1592461708-1311944522.1592461708)

### Set up authentication
Any client application that uses the API must be authenticated and granted access to the requested resources. This section describes important authentication concepts and provides steps for setting it up. For more information, see the [GCP authentication overview](https://cloud.google.com/docs/authentication).

### About service accounts
There are multiple options for authentication, but it is recommended that you use service accounts for authentication and access control. A service account provides credentials for applications, as opposed to end-users. Projects own their service accounts. You can create many service accounts for a project. For more information, see [Service accounts](https://cloud.google.com/docs/authentication#service_accounts).

### About service account keys
Service accounts are associated with one or more public/private key pairs. When you create a new key pair, you download the private key. The Cloud SDK uses your private key to generate credentials when calling the API. You are responsible for security of the private key and other management operations, such as key rotation.

### Create a service account and download the private key file

Set up authentication:
1. In the Cloud Console, go to the [**Create service account key**](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.138544115.1169747201.1592461708-1311944522.1592461708) page.
2. From the **Service account** list, select **New service account**.
3. In the **Service account name** field, enter a name.
4. From the **Role** list, select **Project > Owner**.
5. Click **Create**. A JSON file that contains your key downloads to your computer.

### Use the service account key file in your environment

Provide authentication credentials to your application code by setting the environment variable GOOGLE_APPLICATION_CREDENTIALS. Replace [PATH] with the file path of the JSON file that contains your service account key, and [FILE_NAME] with the filename. This variable only applies to your current shell session, so if you open a new session, set the variable again.

```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
For example:
```
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"
```

### Install and initialize the Cloud SDK

If you plan to use the Vision API, you must install and initialize the Cloud SDK. Cloud SDK is a set of tools that you can use to manage resources and applications hosted on GCP. This includes the gcloud command line tool. The following link provides instructions:

[Install and initialize the Cloud SDK](https://cloud.google.com/sdk/docs).

## Setting up the project:
Create a new conda environment with the following command:

`conda env create -f environment.yml`

Activate environment:

`source activate amplify`

## Library APIs

### WorldCat

https://www.oclc.org/developer/develop/web-services/worldcat-search-api.en.html

### Library Hub

https://discover.libraryhub.jisc.ac.uk/

### ABIM

Link: http://indianmedicine.eldoc.ub.rug.nl/

ABIM supports OAI 2.0 with a base URL of http://indianmedicine.eldoc.ub.rug.nl/cgi/oai2.
More information on OAI protocol: http://www.openarchives.org/OAI/openarchivesprotocol.html
