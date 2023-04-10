README-

## A brief project description

This repository fetches some simple stock price data for 2 companies using the free API from AlphaVantage  locally and makes it accessible via a RESTful web API interface.

## Financial data API- 
Inputs:
* Optional parameters: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), and symbol (string) which represents the company name.
* Optional pagination parameters: limit (integer) and page (integer)
Outputs:
* A JSON response containing the following three properties:
    * data: an array of financial data records that match the provided filters
    * pagination: an object containing pagination information, including the total count of records, current page index, limit, and total number of pages
    * info: an object containing any error information if applicable
Note: If no filters are provided, all financial data records will be returned. The default limit for one page is 5 records.


## Statistics API- 

Inputs:
* Required parameters: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), and symbol (string) which represents the company name. Outputs:
* A JSON response containing the following two properties:
    * data: an object containing the calculated statistic results for the given period, including the average daily open price, average daily closing price, and average daily volume
    * info: an object containing any error information if applicable
Note: All parameters are required, and the endpoint performs calculations on the data within the specified period of time.


## Tech Stack
* Flask: a lightweight Python web framework for building RESTful APIs and web applications.
* Flask-SQLAlchemy: an extension for Flask that simplifies the use of SQLAlchemy for database integration.
* Docker: a platform for building, shipping, and running applications in containers that provide isolation and portability.
* Docker Compose: a tool for defining and running multi-container Docker applications, allowing you to run the whole application stack with a single command.
* postgres:14.1-alpine: A lightweight Docker image based on Alpine Linux with PostgreSQL 14.1 installed.
* python:3.9.6-slim-buster: A slim Docker image based on Debian Buster with Python 3.9.6 installed.


## How to run your code in local environment

1. Make sure you have Docker and Docker Compose installed in your local environment.
2. Run `docker-compose build` to build the containers.
3. Run `docker-compose up` to start the containers and run the application.

## To first populate the database-
* Open a terminal into the docker container for the python application (using docker desktop or CLI)
* Run the python script get_raw_data.py


## Handling of sensitive data-
* The api key is store in a .env file in the financial/ folder. This is good enough for local environment.
* For production environment, if we are using a cloud hosting service such as google cloud, we could store such a file as an encrypted secret and then mount it to the docker image for the api in the docker compose file.
