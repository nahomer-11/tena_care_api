#!/usr/bin/env bash

set -o errexit  # Exit on error

# Log the deployment start
echo "Starting deployment..."

# Upgrade pip
python3 -m pip install --upgrade pip

# Install required dependencies from requirements.txt
pip3 install -r requirements.txt

# Run database migrations (important step for Django setup)
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input


# Start the Gunicorn server
echo "Starting Gunicorn server..."
gunicorn TenaCareAPI.wsgi:application --bind 0.0.0.0:$PORT

