#!/bin/bash

# Build script for Render deployment

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements-deploy.txt

echo "Setting up database..."
python -c "
from app.core.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print('Database tables created successfully')
"

echo "Build completed successfully!" 