#!/bin/bash

# Startup script for Azure App Service
# This script is executed when the container starts

echo "Starting BP Calculator application..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations if needed (for future use)
# python manage.py migrate

# Start Gunicorn server
echo "Starting Gunicorn..."
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=4 app:app
