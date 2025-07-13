import pytest
from fastapi.testclient import TestClient
from inventory_api import app
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_add_user():
    user = {"username": "alice", "email": "alice@example.com"}
    response = client.post("/users", json=user)
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "alice"

def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_inventory():
    item = {
        "id": str(uuid4()),
        "name": "Widget Adapter",
        "releaseDate": datetime.now().isoformat(),
        "manufacturer": {
            "name": "ACME Corporation",
            "homePage": "https://www.acme-corp.com",
            "phone": "408-867-5309"
        }
    }
    response = client.post("/inventory", json=item)
    assert response.status_code == 201
    assert response.json()["message"] == "item created"

def test_search_inventory():
    response = client.get("/inventory?searchString=Widget")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_user():
    # Add a user to delete
    user = {"username": "bob", "email": "bob@example.com"}
    client.post("/users", json=user)
    response = client.delete("/users", params={"userId": "bob"})
    assert response.status_code == 204

def test_get_user_info():
    user = {"username": "carol", "email": "carol@example.com"}
    client.post("/users", json=user)
    response = client.get("/users/carol")
    assert response.status_code == 200
    assert response.json()["username"] == "carol" 