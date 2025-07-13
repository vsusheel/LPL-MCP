import requests
import pytest
import time

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def user_id():
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
    yield data["id"]
    # Teardown: delete the user after tests
    requests.delete(f"{BASE_URL}/users/{data['id']}")


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
        "name": "Test User 2",
        "email": "test2@example.com",
        "age": 28,
        "is_active": True,
    }
    response = requests.post(
        f"{BASE_URL}/users",
        json=user_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    print(f"✅ User created: ID {data['id']}, Name: {data['name']}")
    # Cleanup
    requests.delete(f"{BASE_URL}/users/{data['id']}")


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
    assert data["name"] == update_data["name"]
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