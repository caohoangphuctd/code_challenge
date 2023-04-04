# Bash to execute commands
.SHELL := /usr/bin/bash -e


# Source directory
SOURCE_DIR = app

# Python variables
VENV_DIR = venv
VENV_ACTIVATE = . $(VENV_DIR)/bin/activate


help: # Show help
	@echo "Available commands:"
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; \
		{printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

venv: # Create virtual environment for python3.x
	@[ -d $(VENV_DIR) ] || python3 -m venv $(VENV_DIR)
	@$(VENV_ACTIVATE) && python3 -m pip install -r requirements.txt

run: # Run app locally
	@$(VENV_ACTIVATE)
	@uvicorn --reload app.main:app

create_migration: # Create migration version Ex: make create_migration message=....
	@$(VENV_ACTIVATE)
	@alembic revision --autogenerate -m "$(message)"
