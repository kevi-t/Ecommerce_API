#!/bin/bash

# Ensure Python is installed
echo "Ensuring Python version 3.9 is available..."
python3.9 --version || { echo "Python 3.9 not found!"; exit 1; }

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.9 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install pip (if missing)
echo "Ensuring pip is installed..."
python3.9 -m ensurepip --default-pip
python3.9 -m pip install --upgrade pip

# Build the project
echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput

echo "Applying migrations..."
python3.9 manage.py migrate --noinput

# Show migrations to confirm
echo "Listing migrations..."
python3.9 manage.py showmigrations

echo "Build process completed successfully."