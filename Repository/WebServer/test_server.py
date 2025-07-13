import requests
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ Health check passed: {data['status']}")


def test_root_endpoint():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ Root endpoint: {data['message']}")


def test_create_user():
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "is_active": True,
    }
    response = requests.post(
        f"{BASE_URL}/users",
        json=user_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    data = response.json()
    print(f"✅ User created: ID {data['id']}, Name: {data['name']}")
    return data["id"]


def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    users = response.json()
    print(f"✅ Retrieved {len(users)} users")


def test_get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    print(f"✅ Retrieved user: {user['name']} (ID: {user['id']})")


def test_update_user(user_id):
    update_data = {
        "name": "Updated Test User",
        "email": "updated@example.com",
        "age": 30,
        "is_active": True,
    }
    response = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json=update_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✅ User updated: {data['name']}")


def test_analytics():
    response = requests.get(f"{BASE_URL}/analytics")
    assert response.status_code == 200
    data = response.json()
    print(
        f"✅ Analytics: {data['total_users']} total users, {data['active_users']} active"
    )


def test_delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 204
    print(f"✅ User {user_id} deleted successfully")


def run_all_tests():
    print("🚀 Starting LPL-MCP Web Server Tests")
    print("=" * 50)
    tests_passed = 0
    total_tests = 8
    try:
        test_health_check()
        tests_passed += 1
    except AssertionError:
        print("❌ Health check failed")
    try:
        test_root_endpoint()
        tests_passed += 1
    except AssertionError:
        print("❌ Root endpoint failed")
    user_id = None
    try:
        user_id = test_create_user()
        tests_passed += 1
    except AssertionError:
        print("❌ User creation failed")
    try:
        test_get_users()
        tests_passed += 1
    except AssertionError:
        print("❌ Get users failed")
    if user_id:
        try:
            test_get_user(user_id)
            tests_passed += 1
        except AssertionError:
            print("❌ Get user failed")
        try:
            test_update_user(user_id)
            tests_passed += 1
        except AssertionError:
            print("❌ Update user failed")
    try:
        test_analytics()
        tests_passed += 1
    except AssertionError:
        print("❌ Analytics failed")
    if user_id:
        try:
            test_delete_user(user_id)
            tests_passed += 1
        except AssertionError:
            print("❌ Delete user failed")
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    if tests_passed == total_tests:
        print("🎉 All tests passed! The server is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for more details.")
    return tests_passed == total_tests

if __name__ == "__main__":
    print("⏳ Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    success = run_all_tests()
    exit(0 if success else 1) 