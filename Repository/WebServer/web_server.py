from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from datetime import datetime
import os
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for request/response validation
class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    is_active: bool = Field(True, description="Whether the user is active")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    is_active: bool
    created_at: datetime


class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime: float


# In-memory storage (replace with database in production)
users_db: Dict[int, User] = {}
user_counter = 1


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI server...")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI server...")


# Create FastAPI app instance
app = FastAPI(
    title="LPL-MCP Web Server",
    description="A modern FastAPI web server with comprehensive features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency for getting current user (placeholder for authentication)
async def get_current_user():
    # This would typically validate JWT tokens or session data
    return {"user_id": "demo_user"}


# Root endpoint
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint returning welcome message"""
    return {
        "message": "Welcome to LPL-MCP Web Server!",
        "docs": "/docs",
        "health": "/health",
    }


# Health check endpoint
@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        uptime=0.0,  # You could track actual uptime here
    )


# Users endpoints
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Create a new user"""
    global user_counter

    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Create new user
    user.id = user_counter
    user_counter += 1
    users_db[user.id] = user

    logger.info(f"Created user with ID: {user.id}")

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
    )


@app.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Dict[str, str] = Depends(get_current_user),
):
    """Get all users with pagination"""
    users = list(users_db.values())[skip : skip + limit]
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            is_active=user.is_active,
            created_at=datetime.utcnow(),
        )
        for user in users
    ]


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = users_db[user_id]
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
    )


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: User):
    """Update a user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if email is being changed and if it conflicts
    if user_update.email != users_db[user_id].email:
        for existing_user in users_db.values():
            if existing_user.id != user_id and existing_user.email == user_update.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

    # Update user
    user_update.id = user_id
    users_db[user_id] = user_update

    logger.info(f"Updated user with ID: {user_id}")

    return UserResponse(
        id=user_update.id,
        name=user_update.name,
        email=user_update.email,
        age=user_update.age,
        is_active=user_update.is_active,
        created_at=datetime.utcnow(),
    )


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    del users_db[user_id]
    logger.info(f"Deleted user with ID: {user_id}")


# Analytics endpoint
@app.get("/analytics")
async def get_analytics():
    """Get basic analytics about the system"""
    total_users = len(users_db)
    active_users = sum(1 for user in users_db.values() if user.is_active)

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "timestamp": datetime.utcnow(),
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "web_server:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info",
    )
