#!/usr/bin/env python3
"""
Test script to verify API endpoints are working
"""

import requests
import json

def test_api_endpoints():
    """Test the main API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Scriptodon API Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Get input sources
    print("\n2. Testing get input sources...")
    try:
        response = requests.get(f"{base_url}/api/input-sources/")
        if response.status_code == 200:
            sources = response.json()
            print(f"✅ Found {len(sources)} input sources")
            for source in sources:
                print(f"   - {source['name']} (ID: {source['id']})")
        else:
            print(f"❌ Get input sources failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get input sources error: {e}")
    
    # Test 3: Test script generation endpoint (if we have input sources)
    print("\n3. Testing script generation endpoint...")
    try:
        response = requests.get(f"{base_url}/api/input-sources/")
        if response.status_code == 200:
            sources = response.json()
            if sources:
                # Test with the first input source
                source_id = sources[0]['id']
                print(f"   Testing with input source ID: {source_id}")
                
                # First check if there are test cases
                test_response = requests.get(f"{base_url}/api/test-generation/test-cases/{source_id}")
                if test_response.status_code == 200:
                    test_cases = test_response.json()
                    if test_cases:
                        print(f"   Found {len(test_cases)} test cases")
                        
                        # Try to generate a script
                        script_response = requests.post(
                            f"{base_url}/api/script-output/generate/{source_id}",
                            params={"script_type": "playwright_python"}
                        )
                        
                        if script_response.status_code == 200:
                            print("✅ Script generation successful!")
                        else:
                            print(f"❌ Script generation failed: {script_response.status_code}")
                            print(f"   Error: {script_response.text}")
                    else:
                        print("   ⚠️  No test cases found - need to generate test cases first")
                else:
                    print(f"   ❌ Failed to get test cases: {test_response.status_code}")
            else:
                print("   ⚠️  No input sources found - create one first")
        else:
            print(f"❌ Failed to get input sources: {response.status_code}")
    except Exception as e:
        print(f"❌ Script generation test error: {e}")

def main():
    print("🚀 Scriptodon API Test")
    print()
    
    test_api_endpoints()
    
    print("\n📝 Next steps:")
    print("1. Create an input source (Swagger, Jira, or User Prompt)")
    print("2. Generate test cases for the input source")
    print("3. Generate a script from the test cases")
    print("4. The workflow should be: Input Source → Test Cases → Script")

if __name__ == "__main__":
    main() 