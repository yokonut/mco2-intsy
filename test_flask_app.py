#!/usr/bin/env python3
"""
Test the Flask app to verify frontend connectivity
"""

import requests
import json

def test_flask_app():
    """Test the Flask app endpoints"""
    base_url = "http://localhost:5000"
    
    print("=== Testing Flask App Connectivity ===\n")
    
    # Test 1: Check if the app is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"1. Home page status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Home page is accessible")
        else:
            print("   ❌ Home page not accessible")
    except requests.exceptions.ConnectionError:
        print("   ❌ Flask app is not running. Start it with: python app.py")
        return
    
    # Test 2: Check chat page
    try:
        response = requests.get(f"{base_url}/chat")
        print(f"2. Chat page status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Chat page is accessible")
        else:
            print("   ❌ Chat page not accessible")
    except Exception as e:
        print(f"   ❌ Error accessing chat page: {e}")
    
    # Test 3: Test POST requests to chat endpoint
    test_inputs = [
        "Sarah is the mother of Mike",
        "Are Mike and Emma siblings?",
        "John is the father of Emma",
        "Is Sarah the mother of Alice?",
        "Invalid relationship test"
    ]
    
    print("\n3. Testing POST requests to /chat:")
    for user_input in test_inputs:
        try:
            response = requests.post(
                f"{base_url}/chat",
                data={"query": user_input},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Input: '{user_input}'")
                    print(f"   Response: '{data.get('response', 'No response')}'")
                    
                    # Check if response contains emojis
                    response_text = data.get('response', '')
                    if any(emoji in response_text for emoji in ["✅", "❌", "📌", "🤔", "❓"]):
                        print("   ✅ Response contains emoji")
                    else:
                        print("   ⚠️  Response does not contain emoji")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response: {response.text}")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 50)

def test_local_function():
    """Test the handle_user_input function locally"""
    print("\n=== Testing Local Function ===\n")
    
    try:
        from interface import handle_user_input
        
        test_inputs = [
            "Sarah is the mother of Mike",
            "Are Mike and Emma siblings?",
            "John is the father of Emma",
            "Is Sarah the mother of Alice?",
            "Invalid relationship test"
        ]
        
        for user_input in test_inputs:
            try:
                response = handle_user_input(user_input)
                print(f"Input: '{user_input}'")
                print(f"Response: '{response}'")
                
                # Check if response contains emojis
                if any(emoji in response for emoji in ["✅", "❌", "📌", "🤔", "❓"]):
                    print("✅ Response contains emoji")
                else:
                    print("⚠️  Response does not contain emoji")
                    
            except Exception as e:
                print(f"❌ Error processing '{user_input}': {e}")
            
            print("-" * 50)
            
    except ImportError as e:
        print(f"❌ Cannot import handle_user_input: {e}")

if __name__ == "__main__":
    print("Testing ChatBunny Flask App Connectivity")
    print("=" * 50)
    
    # Test local function first
    test_local_function()
    
    # Test Flask app
    test_flask_app()
    
    print("\n=== Test Summary ===")
    print("✅ Local function test completed")
    print("🤖 Flask app connectivity test completed")
    print("📌 Check if responses contain emojis like 📌✅❌🤔")
    print("🎯 If emojis are present, the system is working correctly!") 