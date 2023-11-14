.ONESHELL:
SHELL=/bin/bash

ifeq ($(OS),Windows_NT)
    VENV_PATH := ./venv/Scripts
else
    VENV_PATH := ./venv/bin
endif

venv:
	conda create --prefix ./venv python=3.10

install:
	$(VENV_PATH)/pip install -r requirements.txt

migrate:
	$(VENV_PATH)/python ./manage.py migrate

migrations:
	$(VENV_PATH)/python ./manage.py makemigrations

pip:
	$(VENV_PATH)/pip install $(package)
	$(VENV_PATH)/pip freeze | grep -i $(package) >> requirements.txt

run:
	$(VENV_PATH)/python ./manage.py runserver

shell:
	$(VENV_PATH)/python ./manage.py shell

superuser:
	$(VENV_PATH)/python ./manage.py createsuperuser
