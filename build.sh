#!/bin/bash

# Install pip (if missing)
echo "Ensuring pip is installed..."
python3.9 -m ensurepip --default-pip
python3.9 -m pip install --upgrade pip

# Build the project
echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear
