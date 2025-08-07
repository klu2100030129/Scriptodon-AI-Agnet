#!/bin/bash
echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Installing dependencies from requirements.txt..."

# Upgrade pip
pip install --upgrade pip

# Install greenlet first with pre-compiled wheel
pip install greenlet==2.0.2 --only-binary=all --no-cache-dir

# Install requirements with no cache
pip install -r requirements.txt --only-binary=all --no-cache-dir

echo "Build completed successfully!" 