# Project Name

## Overview
This project is a Python-based application that includes a server and data clients. It is designed to handle data retrieval, sorting, and error handling from multiple data sources.

## Features
- **Data Retrieval**: Fetches data from multiple sources.
- **Error Handling**: Gracefully handles errors and timeouts from data sources.
- **Data Sorting**: Sorts data from multiple sources.

## Installation
Create a virtual environment and use poetry to install the dependencies:
```sh
python -m venv .venv
source venv/bin/activate
pip install poetry
poetry install
```

## Preparing the Data
To prepare the database:
```sh
docker-compose up -d
```
To fill the database with data use [fill_data.py](db/fill_data.py)
```sh
export PYTHONPATH=.
python db/fill_data.py
```
The database should now be filled with data:

![db.png](media/db.png)

## Running the Server
Setup .env file with needed environment variables, for example:
```dotenv
DB1_URL=postgresql+asyncpg://irusland:password@0.0.0.0:5432/db
```

To start the server, run:
```sh
make run
```
Use swagger to interact with the API:

![api.png](media/api.png)

## Running the Tests
To run the tests, run:
```sh
make test
```
see test.env for test environment variables

## Development
To run formatters:
```sh
make format
```

## Author
Ruslan Sirazhetdinov ([irusland](github.com/irusland))
