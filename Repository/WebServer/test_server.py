#!/usr/bin/env python3
"""
Test script for the LPL-MCP FastAPI Web Server
Run this script to test the basic functionality of the server
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# Server configuration
BASE_URL = "http://localhost:8000"

def test_health_check() -> bool:
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")
        return False

def test_root_endpoint() -> bool:
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data['message']}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_create_user() -> Optional[int]:
    """Test creating a user and return the user ID"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "is_active": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ User created: ID {data['id']}, Name: {data['name']}")
            return data['id']
        else:
            print(f"❌ User creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return None

def test_get_users() -> bool:
    """Test getting all users"""
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Retrieved {len(users)} users")
            return True
        else:
            print(f"❌ Get users failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get users error: {e}")
        return False

def test_get_user(user_id: int) -> bool:
    """Test getting a specific user"""
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Retrieved user: {user['name']} (ID: {user['id']})")
            return True
        else:
            print(f"❌ Get user failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get user error: {e}")
        return False

def test_update_user(user_id: int) -> bool:
    """Test updating a user"""
    update_data = {
        "name": "Updated Test User",
        "email": "updated@example.com",
        "age": 30,
        "is_active": True
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/users/{user_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User updated: {data['name']}")
            return True
        else:
            print(f"❌ User update failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User update error: {e}")
        return False

def test_analytics() -> bool:
    """Test the analytics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/analytics")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analytics: {data['total_users']} total users, {data['active_users']} active")
            return True
        else:
            print(f"❌ Analytics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return False

def test_delete_user(user_id: int) -> bool:
    """Test deleting a user"""
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 204:
            print(f"✅ User {user_id} deleted successfully")
            return True
        else:
            print(f"❌ User deletion failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User deletion error: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Starting LPL-MCP Web Server Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 7
    
    # Test 1: Health check
    if test_health_check():
        tests_passed += 1
    
    # Test 2: Root endpoint
    if test_root_endpoint():
        tests_passed += 1
    
    # Test 3: Create user
    user_id = test_create_user()
    if user_id:
        tests_passed += 1
    
    # Test 4: Get all users
    if test_get_users():
        tests_passed += 1
    
    # Test 5: Get specific user
    if user_id and test_get_user(user_id):
        tests_passed += 1
    
    # Test 6: Update user
    if user_id and test_update_user(user_id):
        tests_passed += 1
    
    # Test 7: Analytics
    if test_analytics():
        tests_passed += 1
    
    # Test 8: Delete user (cleanup)
    if user_id and test_delete_user(user_id):
        tests_passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The server is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for more details.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    # Wait a moment for server to start if needed
    print("⏳ Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    success = run_all_tests()
    exit(0 if success else 1) 