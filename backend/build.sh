#!/bin/bash
echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Installing dependencies from requirements.txt..."

# Upgrade pip
pip install --upgrade pip

# Install greenlet first with pre-compiled wheel
pip install greenlet==3.0.3 --only-binary=all --no-cache-dir

# Install requirements with no cache
pip install -r requirements.txt --no-cache-dir

echo "Build completed successfully!" 