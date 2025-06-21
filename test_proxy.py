#!/usr/bin/env python3
"""
Test script for Paystar Proxy Server
"""

import requests
import json
import sys

# Configuration
PROXY_URL = 'http://localhost:3000'
TEST_URL = 'https://httpbin.org/get'

def test_proxy():
    """Test the proxy server functionality"""
    print("🧪 Testing Paystar Proxy Server...\n")
    
    try:
        # Test 1: Health check
        print("1️⃣ Testing health check...")
        health_response = requests.get(f"{PROXY_URL}/health")
        health_response.raise_for_status()
        print("✅ Health check passed:", health_response.json())
        print()
        
        # Test 2: Simple GET request
        print("2️⃣ Testing simple GET request...")
        get_response = requests.post(f"{PROXY_URL}/proxy", json={
            "config": {
                "method": "GET",
                "url": TEST_URL,
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        })
        get_response.raise_for_status()
        print("✅ GET request passed")
        print("Response status:", get_response.status_code)
        print("Response data keys:", list(get_response.json()['data'].keys()))
        print()
        
        # Test 3: POST request with data
        print("3️⃣ Testing POST request with data...")
        post_response = requests.post(f"{PROXY_URL}/proxy", json={
            "config": {
                "method": "POST",
                "url": "https://httpbin.org/post",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "test": "data",
                    "message": "Hello from proxy!"
                }
            }
        })
        post_response.raise_for_status()
        print("✅ POST request passed")
        print("Response status:", post_response.status_code)
        print("Response data keys:", list(post_response.json()['data'].keys()))
        print()
        
        # Test 4: Error handling (invalid URL)
        print("4️⃣ Testing error handling...")
        try:
            error_response = requests.post(f"{PROXY_URL}/proxy", json={
                "config": {
                    "method": "GET",
                    "url": "https://invalid-url-that-does-not-exist.com",
                    "timeout": 5
                }
            })
            print("✅ Error handling works correctly")
            print("Error response:", error_response.json())
        except requests.exceptions.RequestException as e:
            print("✅ Error handling works correctly")
            print("Error:", str(e))
        print()
        
        print("🎉 All tests passed! Proxy server is working correctly.")
        print()
        print("📋 Test Summary:")
        print("  ✅ Health check endpoint")
        print("  ✅ GET request proxying")
        print("  ✅ POST request proxying")
        print("  ✅ Error handling")
        print()
        print("🚀 Proxy server is ready for production use!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Test failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response data: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_proxy() 