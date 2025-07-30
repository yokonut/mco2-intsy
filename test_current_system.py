#!/usr/bin/env python3
"""
Test the current ChatBunny system without modifying existing files
"""

from interface import handle_user_input, family
from relationships import *

def test_current_system():
    """Test the current system to see how it works"""
    print("=== Testing Current ChatBunny System ===\n")
    
    # Test 1: Check what's currently in the knowledge base
    print("1. Current knowledge base:")
    try:
        males = list(family.query("male(X)"))
        females = list(family.query("female(X)"))
        parents = list(family.query("parent_of(X, Y)"))
        print(f"   Males: {males}")
        print(f"   Females: {females}")
        print(f"   Parents: {parents}")
    except Exception as e:
        print(f"   Error querying knowledge base: {e}")
    
    print("\n2. Testing relationship functions:")
    
    # Test mother function
    print("\n   Testing mother('sarah', 'mike'):")
    try:
        assertions = mother("sarah", "mike")
        print(f"   Assertions returned: {assertions}")
        result = assertz(assertions)
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test father function
    print("\n   Testing father('john', 'emma'):")
    try:
        assertions = father("john", "emma")
        print(f"   Assertions returned: {assertions}")
        result = assertz(assertions)
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test sibling function
    print("\n   Testing sibling('mike', 'emma'):")
    try:
        result = sibling("mike", "emma")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. Testing handle_user_input function:")
    
    # Test statements
    test_inputs = [
        "Sarah is the mother of Mike",
        "John is the father of Emma", 
        "Are Mike and Emma siblings?",
        "Is Sarah the mother of Mike?",
        "Invalid input test"
    ]
    
    for user_input in test_inputs:
        print(f"\n   Input: '{user_input}'")
        try:
            response = handle_user_input(user_input)
            print(f"   Response: {response}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n4. Testing Prolog queries directly:")
    
    # Test some direct Prolog queries
    queries = [
        "siblings(mike, emma)",
        "mother_of(sarah, mike)",
        "father_of(john, emma)",
        "parent_of(sarah, mike)"
    ]
    
    for query in queries:
        try:
            results = list(family.query(query))
            print(f"   Query '{query}': {results}")
        except Exception as e:
            print(f"   Query '{query}' error: {e}")

def test_frontend_connectivity():
    """Test how the frontend would interact with the backend"""
    print("\n=== Frontend Connectivity Test ===\n")
    
    # Simulate what the frontend sends
    frontend_inputs = [
        "Sarah is the mother of Mike",
        "Are Mike and Emma siblings?",
        "John is the father of Emma",
        "Is Sarah the mother of Alice?",
        "Invalid relationship test"
    ]
    
    for user_input in frontend_inputs:
        print(f"Frontend sends: '{user_input}'")
        try:
            response = handle_user_input(user_input)
            print(f"Backend responds: '{response}'")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 50)

if __name__ == "__main__":
    test_current_system()
    test_frontend_connectivity()
    
    print("\n=== Summary ===")
    print("✅ System test completed!")
    print("📌 Check the responses above to see if emoji responses are working")
    print("🤖 Frontend connectivity can be verified by running the Flask app")
    print("🎯 If responses contain emojis like 📌✅❌🤔, the system is working correctly") 