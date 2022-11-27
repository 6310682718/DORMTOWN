#!/bin/sh
python3 manage.py makemigrations
python3 manage.py makemigrations chat
python3 manage.py makemigrations occupant
python3 manage.py migrate
