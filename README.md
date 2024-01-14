# Content Management System
Built API for Content Management System

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
  - [Virtual Environment](#virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Run Using Docker](#run-using-docker)
- [Using Postman](#postman)
- [Fixtures and Seeding](#fixtures-and-seeding)
- [Running Tests](#running-tests)
- [Code Coverage](#code-coverage)

## Introduction

Content Management System is an API for Creating, editing, deleting, viewing and searching content created by the user. Authentication and authorisation are also added to the project.

## Features

- The system will have 2 types of user role, admin and author. Admin users are created
using seeding
- Author should be able to register and login using email to the CMS (Refer below table for
user fields)
- Admin can view, edit and delete all the contents created by multiple authors
- Author can create, view, edit and delete contents created by him only
- Users should search content by matching terms in title, body, summary and categories.

## Setup

Follow these steps to set up your development environment.

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (3.8 or higher)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Virtual Environment

1. Create and activate a virtual environment in your project's root directory:

    ```bash
    python -m venv venv
    ```

    - On Windows:

      ```bash
      .\venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Database Setup

```bash
python manage.py migrate
```
> [!NOTE]
> We are using sqlite database for to get work done easily. You can setup your own database by changing DATABASES variable example:

Lets we want to use postgresql
```python
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': ‘<database_name>’,
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
```
also you need to install respective library for this. In our case you have to enter command
```bash
pip install psycopg2
```

## Running the Application

To run the project, follow these steps:

### Start the Development Server

1. In your project's root directory, activate the virtual environment:

    - On Windows:

      ```bash
      .\venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

2. Start the development server:

    ```bash
    python manage.py runserver
    ```

3. Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) to access the application.

### Example Use Case

Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) will list all the api routes for you

### Stop the Server

To stop the development server, press `Ctrl + C` in the terminal.

[Include any additional instructions or information related to running your specific Django application.]

## Using Postman
- Attached Postman collections file in the project. [CMS.postman_collection.json](./CMS.postman_collection.json). Can use for testing purpose.

## Run Using Docker
We Also build a Docker image for this application also added the [docker file](./Dockerfile) in this repository. [click here](https://hub.docker.com/repository/docker/sunnybhagwat/arcitech-cms) to see repository.


-If you don't already have Docker installed on your server, please follow the steps on [Docker CE for Ubuntu](https://docs.docker.com/engine/install/ubuntu/) to install Docker.

You can also install Docker using the (docker-install)[https://github.com/docker/docker-install] script which is(supported linux distros only):
```bash
curl -fsSL https://get.docker.com | sh
```



If you want to run the application to you system directly with the docker, use following command:
```bash 
docker run -p 8000:8000 sunnybhagwat/arcitech-cms:latest
```
- Also if you want go and build the on your machine you do that too with following command:
```bash
docker build -t arcitech-cms .
```
> [!NOTE]
> You can change arcitech-cms with name you want as you image name

- Now to run this locally built image:
```bash
docker run -p 8000:8000 --name cms arcitech-cms
```
> [!NOTE]
> You can replace cms with with the name you want and make sure to replace arcitech-cms to the name you gave while building the image.

-To run same in detachable mode add -d before --name option. So the command will be:
```bash
docker run -p 8000:8000 -d --name cms arcitech-cms
```

## Fixtures and Seeding

To seed the database with Admin usera, you can use Django fixtures. . Follow these steps:    

### Create Fixture
1. We have already created fixtures so no to create new.
To edit details change email, password and other deatils you want with changing schema [admin_users_fixture.json](main/fixtures/admin_users_fixture.json).

2. After edting make sure if you sett the  plain text password run the following comamnd to hash the passwords:
```bash
python manage.py hash_passwords main/fixtures/admin_users_fixture.json
```

### Load Fixtures

3. Load the fixture data into the database:
    
    ```bash
    python3 manage.py loaddata main/fixtures/admin_users_fixture.json
    ```

### Verify Data

3. Verify that the data has been successfully loaded into the database.

### Resetting the Database

If you need to reset the database and reapply migrations, you can use the following commands:

```bash
python manage.py flush
python manage.py migrate
python manage.py loaddata path/to/your/fixtures.json
```

## Running Tests

To ensure the stability and correctness, we can run tests using Django's testing framework. Follow these steps:

### Run Tests

1. In your project's root directory, activate the virtual environment:

    follow [Virtual Environment](#virtual-environment)

2. Run the tests using the following command:

    ```bash
    python manage.py test
    ```

### Code Coverage

For code coverage analysis, you can use the `coverage` tool. Also we have added [coverarge folder named as htmlcov](htmlcov/) as htmlcov Follow these steps:

1. Run the tests with coverage:

    ```bash
    coverage run manage.py test
    ```

2. Generate and view the coverage report:

    ```bash
    coverage html
    ```

    Open `htmlcov/index.html` in a browser to view the coverage report.


