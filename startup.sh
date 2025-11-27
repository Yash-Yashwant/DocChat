#!/bin/bash
# GCP VM Startup Script for DocChat Backend
# This script sets up the environment and runs the FastAPI application

set -e  # Exit on error

echo "=== DocChat Backend Setup ==="

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git

# Navigate to app directory
APP_DIR="/home/$USER/DocChat"
cd $APP_DIR

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Google Cloud SDK if not present
if ! command -v gcloud &> /dev/null; then
    echo "Installing Google Cloud SDK..."
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
fi

echo "=== Setup Complete ==="
echo "To start the server manually, run:"
echo "  source venv/bin/activate"
echo "  uvicorn fastApi.api:app --host 0.0.0.0 --port 8000"
