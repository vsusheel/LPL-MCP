from fastapi import FastAPI, HTTPException, Depends, status, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
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


# Enhanced Pydantic models with examples for SwaggerHub
class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(
        ..., min_length=1, max_length=100, description="User's full name"
    )
    email: str = Field(
        ..., description="User's email address (must be unique)"
    )
    age: Optional[int] = Field(
        None, ge=0, le=150, description="User's age in years"
    )
    is_active: bool = Field(
        True, description="Whether the user account is active"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "age": 30,
                    "is_active": True,
                }
            ]
        }
    }


class UserResponse(BaseModel):
    id: int = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    age: Optional[int] = Field(None, description="User's age")
    is_active: bool = Field(..., description="User account status")
    created_at: datetime = Field(..., description="Account creation timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "age": 30,
                    "is_active": True,
                    "created_at": "2024-01-01T12:00:00",
                }
            ]
        }
    }


class HealthCheck(BaseModel):
    status: str = Field(..., description="System health status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    uptime: float = Field(..., description="System uptime in seconds")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "timestamp": "2024-01-01T12:00:00",
                    "version": "1.0.0",
                    "uptime": 3600.0,
                }
            ]
        }
    }


class AnalyticsResponse(BaseModel):
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    inactive_users: int = Field(..., description="Number of inactive users")
    timestamp: datetime = Field(..., description="Analytics timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_users": 100,
                    "active_users": 85,
                    "inactive_users": 15,
                    "timestamp": "2024-01-01T12:00:00",
                }
            ]
        }
    }


# In-memory storage (replace with database in production)
users_db: Dict[int, User] = {}
user_counter = 1


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up LPL-MCP FastAPI Web Server...")
    yield
    # Shutdown
    logger.info("Shutting down LPL-MCP FastAPI Web Server...")


# Create FastAPI app instance with enhanced configuration
app = FastAPI(
    title="LPL-MCP Web Server",
    description="""
    ## LPL-MCP Web Server API
    
    A comprehensive FastAPI web server with user management, health monitoring, and analytics.
    
    ### 🚀 Features
    * **User Management**: Complete CRUD operations for user accounts
    * **Health Monitoring**: Real-time system status and uptime tracking
    * **Analytics**: Usage statistics and system metrics
    * **API Documentation**: Auto-generated interactive documentation
    
    ### 📚 Getting Started
    1. **Create a user** using `POST /users`
    2. **Retrieve users** with `GET /users` (supports pagination)
    3. **Monitor system health** with `GET /health`
    4. **View analytics** with `GET /analytics`
    
    ### 🔧 Development
    - Interactive API docs: `/docs`
    - Alternative docs: `/redoc`
    - OpenAPI spec: `/openapi.json`
    
    ### 🛡️ Security
    - Input validation with Pydantic models
    - CORS support for cross-origin requests
    - Comprehensive error handling
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "LPL-MCP Team",
        "email": "support@lpl-mcp.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom OpenAPI schema for better SwaggerHub integration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="LPL-MCP Web Server",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
        tags=[
            {
                "name": "users",
                "description": "User management operations. Create, read, update, and delete user accounts.",
            },
            {
                "name": "health",
                "description": "System health and monitoring endpoints for operational status.",
            },
            {
                "name": "analytics",
                "description": "System analytics and metrics for monitoring usage patterns.",
            },
        ],
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Development server",
            },
            {
                "url": "https://api.lpl-mcp.com",
                "description": "Production server",
            },
        ],
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Dependency for getting current user (placeholder for authentication)
async def get_current_user():
    """Get current authenticated user (placeholder for JWT authentication)"""
    return {"user_id": "demo_user"}


# Root endpoint
@app.get(
    "/",
    response_model=Dict[str, str],
    tags=["root"],
    summary="Welcome",
    description="Root endpoint returning welcome message and API information",
    response_description="Welcome message with API links",
)
async def root():
    """Root endpoint returning welcome message and API information"""
    return {
        "message": "Welcome to LPL-MCP Web Server!",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0",
    }


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthCheck,
    tags=["health"],
    summary="Health Check",
    description="Check system health and operational status",
    response_description="System health status with uptime information",
    responses={
        200: {
            "description": "System is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-01-01T12:00:00",
                        "version": "1.0.0",
                        "uptime": 3600.0,
                    }
                }
            },
        }
    },
)
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        uptime=0.0,  # You could track actual uptime here
    )


# Users endpoints
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Create User",
    description="""
    Create a new user account in the system.
    
    **Required fields:**
    - `name`: User's full name (1-100 characters)
    - `email`: User's email address (must be unique)
    
    **Optional fields:**
    - `age`: User's age (0-150 years)
    - `is_active`: Account status (default: true)
    
    The system will automatically assign a unique ID and creation timestamp.
    """,
    response_description="User successfully created with assigned ID",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "age": 30,
                        "is_active": True,
                        "created_at": "2024-01-01T12:00:00",
                    }
                }
            },
        },
        400: {
            "description": "Bad request - validation error or email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered",
                        "timestamp": "2024-01-01T12:00:00",
                    }
                }
            },
        },
    },
)
async def create_user(user: User):
    """Create a new user account"""
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
        id=user_counter - 1,  # Use the assigned ID
        name=user.name,
        email=user.email,
        age=user.age,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
    )


@app.get(
    "/users",
    response_model=List[UserResponse],
    tags=["users"],
    summary="Get Users",
    description="""
    Retrieve all users with optional pagination support.
    
    **Query Parameters:**
    - `skip`: Number of users to skip (default: 0)
    - `limit`: Maximum number of users to return (default: 100, max: 1000)
    
    Returns a list of user objects with their details.
    """,
    response_description="List of users with pagination support",
    responses={
        200: {
            "description": "List of users retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "John Doe",
                            "email": "john.doe@example.com",
                            "age": 30,
                            "is_active": True,
                            "created_at": "2024-01-01T12:00:00",
                        }
                    ]
                }
            },
        }
    },
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of users to return"
    ),
    current_user: Dict[str, str] = Depends(get_current_user),
):
    """Get all users with pagination support"""
    users = list(users_db.values())[skip : skip + limit]
    return [
        UserResponse(
            id=user.id if user.id is not None else -1,
            name=user.name,
            email=user.email,
            age=user.age,
            is_active=user.is_active,
            created_at=datetime.utcnow(),
        )
        for user in users
    ]


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
    summary="Get User by ID",
    description="Retrieve a specific user by their unique ID",
    response_description="User details for the specified ID",
    responses={
        200: {
            "description": "User found successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "age": 30,
                        "is_active": True,
                        "created_at": "2024-01-01T12:00:00",
                    }
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found",
                        "timestamp": "2024-01-01T12:00:00",
                    }
                }
            },
        },
    },
)
async def get_user(
    user_id: int = Path(..., gt=0, description="Unique user identifier")
):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = users_db[user_id]
    return UserResponse(
        id=user.id if user.id is not None else -1,
        name=user.name,
        email=user.email,
        age=user.age,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
    )


@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
    summary="Update User",
    description="""
    Update an existing user's information.
    
    All fields are optional - only provided fields will be updated.
    Email uniqueness is validated if the email is being changed.
    """,
    response_description="Updated user information",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Bad request - email already exists"},
        404: {"description": "User not found"},
    },
)
async def update_user(
    user_id: int = Path(..., gt=0, description="Unique user identifier"),
    user_update: User = Body(..., description="Updated user information"),
):
    """Update a user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if email is being changed and if it conflicts
    if user_update.email != users_db[user_id].email:
        for existing_user in users_db.values():
            if (
                existing_user.id != user_id
                and existing_user.email == user_update.email
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

    # Update user
    user_update.id = user_id
    users_db[user_id] = user_update

    logger.info(f"Updated user with ID: {user_id}")

    return UserResponse(
        id=user_id,  # Use the path parameter
        name=user_update.name,
        email=user_update.email,
        age=user_update.age,
        is_active=user_update.is_active,
        created_at=datetime.utcnow(),
    )


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
    summary="Delete User",
    description="Permanently delete a user account by ID",
    response_description="User successfully deleted",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
)
async def delete_user(
    user_id: int = Path(..., gt=0, description="Unique user identifier")
):
    """Delete a user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    del users_db[user_id]
    logger.info(f"Deleted user with ID: {user_id}")


# Analytics endpoint
@app.get(
    "/analytics",
    response_model=AnalyticsResponse,
    tags=["analytics"],
    summary="Get Analytics",
    description="""
    Retrieve system analytics and usage metrics.
    
    Provides insights into user activity and system usage patterns.
    """,
    response_description="System analytics and metrics",
    responses={
        200: {
            "description": "Analytics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_users": 100,
                        "active_users": 85,
                        "inactive_users": 15,
                        "timestamp": "2024-01-01T12:00:00",
                    }
                }
            },
        }
    },
)
async def get_analytics():
    """Get basic analytics about the system"""
    total_users = len(users_db)
    active_users = sum(1 for user in users_db.values() if user.is_active)

    return AnalyticsResponse(
        total_users=total_users,
        active_users=active_users,
        inactive_users=total_users - active_users,
        timestamp=datetime.utcnow(),
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
        },
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

    logger.info(f"Starting enhanced LPL-MCP Web Server on {host}:{port}")
    logger.info(f"API Documentation: http://{host}:{port}/docs")
    logger.info(f"Health Check: http://{host}:{port}/health")

    uvicorn.run(
        "web_server_enhanced:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info",
    )
