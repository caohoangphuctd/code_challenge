# Regov Project

## Folder Structure

```shell
.
├── question_2 # Code for question 2
│   ├── exercise_1.py # exercise 1
│   ├── exercise_2.py # exercise 2
├── migrations # Migrations database version
├── app # Main logic code
│   ├── apis # The views layer
│   │   ├── __init__.py
│   │   ├── users.py # APIs for users
│   ├── controllers # The controllers layer
│   │   ├── __init__.py
│   │   ├── users.py # Controller for user
│   │   ├── auth.py # Controller for authentication
│   ├── database # The models layer
│   │   ├── __init__.py
│   │   ├── config.py # Config naming convention for database
│   │   ├── depends.py # Add dependency for database
│   │   └── models.py # Declare models
│   │   └── redis.py # Declare models
│   ├── exceptions # The exception layer
│   │   ├── configure_exceptions.py # Config exception
│   │   ├── handle_exceptions.py # Handle exception
│   ├── schemas # The schema layer to validate request/response data
│   │   ├── __init__.py
│   │   ├── users.py
│   ├── common # The common folder
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── password.py
│   │   ├── handle_twilio.py
│   ├── __init__.py
│   ├── __version__.py
│   ├── config.py # Config for main app (paging, database, variables)
│   ├── configure_logging.py # Config for logging
│   ├── main.py # Init app
├── Makefile
├── README.md
├── requirements.in
├── requirements.txt
├── gunicorn.conf.py
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── .pre-commit-config.yaml # format code before commit
├── .gitignore
├── tests # Contains all tests
│   ├── unit_tests
│   │   ├── __init__.py
│   │   ├── data # data folder
```

## Run app locally
```shell
# Follow instructions in [Set up PostgreSQL test database](#set-up-postgresql-test-database)
# to set up test database

# Set up virtual environment
make venv

# Run migration
alembic upgrade head


# Run app
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=admin
export POSTGRES_DB=opusmatch
export POSTGRES_HOST=postgres
export REDIS_HOST="192.168.40.55"
export REDIS_PORT=6379
export ACCOUNT_SID="ACc0880957bf081dff083ffd2135bcaf32"
export AUTH_TOKEN="e57edf3267f4f556c90583517cfcc748"
make run

Open "http://localhost:8000/api/v1#"
```


## Run migration
```shell

# Set up virtual environment
make venv

# import variables
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=admin
export POSTGRES_DB=opusmatch
export POSTGRES_HOST=postgres
export REDIS_HOST="192.168.40.55"
export REDIS_PORT=6379
export ACCOUNT_SID="ACc0880957bf081dff083ffd2135bcaf32"
export AUTH_TOKEN="e57edf3267f4f556c90583517cfcc748"

# Create new migration version
make create_migration message="init regov"

# Run migration
alembic upgrade head
```


## Run docker compose
```shell
# Install docker and docker-compose before run app via docker-compose.yml

docker-compose up -d
Open `http://localhost:8000/api/v1#`
```

# Run Testing
Create new database for test and update in .env file
```
# import variables
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=admin
export POSTGRES_DB=opusmatch
export POSTGRES_HOST=postgres
export REDIS_HOST="192.168.40.55"
export REDIS_PORT=6379
export ACCOUNT_SID="ACc0880957bf081dff083ffd2135bcaf32"
export AUTH_TOKEN="e57edf3267f4f556c90583517cfcc748"
export PYTHONPATH=$PWD:app
```

Run test
```
coverage run --source=./app -m pytest && coverage report -m && coverage html
```


# Run pre-commit
```
pre-commit run --all-files
```
