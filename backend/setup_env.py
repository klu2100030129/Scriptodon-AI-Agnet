#!/usr/bin/env python3
"""
Scriptodon Environment Setup Script

This script helps you set up the required environment variables for Scriptodon.
"""

import os
import sys

def create_env_file():
    """Create a .env file with the required configuration."""
    
    env_content = """# OpenRouter API Configuration
# Get your API key from https://openrouter.ai/keys
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Site Configuration
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_SITE_NAME=Scriptodon Test Automation Platform

# Jira Configuration (optional)
JIRA_SERVER_URL=
JIRA_USERNAME=
JIRA_API_TOKEN=

# Database Configuration
DATABASE_URL=sqlite:///./scritodon.db

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
"""
    
    env_file_path = ".env"
    
    if os.path.exists(env_file_path):
        print(f"⚠️  .env file already exists at {env_file_path}")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file_path}")
        print("\n📝 Next steps:")
        print("1. Edit the .env file and replace 'your_openrouter_api_key_here' with your actual API key")
        print("2. Get your API key from https://openrouter.ai/keys")
        print("3. Restart the backend server")
        print("\n💡 The script generation feature will work once you set up the API key!")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        sys.exit(1)

def main():
    print("🚀 Scriptodon Environment Setup")
    print("=" * 40)
    print()
    print("This script will create a .env file with the required configuration.")
    print("You'll need to get an OpenRouter API key to use the AI features.")
    print()
    
    create_env_file()

if __name__ == "__main__":
    main() 