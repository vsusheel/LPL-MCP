from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import uuid4, UUID
from datetime import datetime

app = FastAPI(title="Simple Inventory API", version="1.0.0", description="This is a simple API")

# Pydantic models
class Manufacturer(BaseModel):
    name: str = Field(..., example="ACME Corporation")
    homePage: Optional[str] = Field(None, example="https://www.acme-corp.com")
    phone: Optional[str] = Field(None, example="408-867-5309")

class InventoryItem(BaseModel):
    id: UUID = Field(default_factory=uuid4, example="d290f1ee-6c54-4b01-90e6-d701748f0851")
    name: str = Field(..., example="Widget Adapter")
    releaseDate: datetime = Field(..., example="2016-08-29T09:12:33.001Z")
    manufacturer: Manufacturer

class User(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")

# In-memory storage
inventory_db: List[InventoryItem] = []
users_db: List[User] = []

# Inventory endpoints
@app.get("/inventory", response_model=List[InventoryItem], tags=["developers"])
def search_inventory(searchString: Optional[str] = Query(None), skip: int = 0, limit: int = 50):
    results = inventory_db
    if searchString:
        results = [item for item in results if searchString.lower() in item.name.lower()]
    return results[skip:skip+limit]

@app.post("/inventory", status_code=201, tags=["admins"])
def add_inventory(item: InventoryItem):
    for inv in inventory_db:
        if inv.id == item.id:
            raise HTTPException(status_code=409, detail="An existing item already exists")
    inventory_db.append(item)
    return {"message": "item created"}

# User endpoints
@app.post("/users", status_code=201, tags=["admins"])
def add_user(user: User):
    for u in users_db:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    users_db.append(user)
    return {"message": f"Hello, {user.username}!", "user": user}

@app.delete("/users", status_code=204, tags=["admins"])
def delete_user(userId: str = Query(...)):
    global users_db
    users_db = [u for u in users_db if u.username != userId and u.email != userId]
    return

@app.get("/users", response_model=List[User], tags=["admins"])
def get_all_users():
    return users_db

@app.get("/users/{userId}", response_model=User, tags=["admins"])
def get_user_info(userId: str = Path(...)):
    for user in users_db:
        if user.username == userId or user.email == userId:
            return user
    raise HTTPException(status_code=404, detail="User not found") 