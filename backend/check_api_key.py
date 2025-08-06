#!/usr/bin/env python3
"""
Script to verify OpenRouter API key configuration
"""

import os
import requests
from app.core.config import settings

def check_api_key():
    """Check if the OpenRouter API key is properly configured and valid."""
    
    print("🔍 Checking OpenRouter API Key Configuration")
    print("=" * 50)
    
    # Check if API key is set
    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        print("❌ OPENROUTER_API_KEY is not set in environment")
        return False
    
    if api_key == "your_openrouter_api_key_here":
        print("❌ OPENROUTER_API_KEY is still set to placeholder value")
        print("   Please update your .env file with your actual API key")
        return False
    
    print(f"✅ API Key is set: {api_key[:10]}...{api_key[-4:]}")
    
    # Test the API key with a simple request
    print("\n🧪 Testing API key with OpenRouter...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_SITE_NAME,
    }
    
    data = {
        "model": "qwen/qwen-2.5-72b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": "Hello, this is a test message."
            }
        ],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API key is valid and working!")
            return True
        elif response.status_code == 401:
            print("❌ API key is invalid or expired")
            print("   Please check your OpenRouter account and regenerate the key")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def main():
    print("🚀 OpenRouter API Key Verification")
    print()
    
    if check_api_key():
        print("\n🎉 Your API key is working correctly!")
        print("   You should now be able to generate test cases and scripts.")
    else:
        print("\n🔧 To fix this issue:")
        print("1. Go to https://openrouter.ai/keys")
        print("2. Check your account status and credits")
        print("3. Generate a new API key if needed")
        print("4. Update your .env file with the new key")
        print("5. Restart the backend server")

if __name__ == "__main__":
    main() 