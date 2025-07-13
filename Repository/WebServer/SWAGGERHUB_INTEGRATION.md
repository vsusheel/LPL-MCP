# SwaggerHub Integration with FastAPI Web Server

## Overview

This guide explains how to integrate **SwaggerHub** with your FastAPI web server for enhanced API design, documentation, and collaboration.

## What is SwaggerHub?

**SwaggerHub** is a cloud-based platform that provides:
- **API Design**: Visual OpenAPI specification editor
- **Documentation**: Auto-generated interactive API docs
- **Collaboration**: Team-based API development
- **Testing**: Built-in API testing and mocking
- **Integration**: CI/CD and code generation

## Current FastAPI OpenAPI Generation

Your FastAPI server automatically generates OpenAPI 3.1.0 specifications:

```bash
# Get the OpenAPI specification
curl http://localhost:8000/openapi.json

# View interactive documentation
# Open in browser: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
```

## Integration Workflows

### 1. **Export Current API to SwaggerHub**

#### Step 1: Export OpenAPI Specification
```bash
# Save current API spec to file
curl -s http://localhost:8000/openapi.json > api-spec.json
```

#### Step 2: Import to SwaggerHub
1. Go to [SwaggerHub](https://swaggerhub.com)
2. Create account/login
3. Click "Import API"
4. Upload your `api-spec.json` file
5. Configure API details (name, version, etc.)

### 2. **Design-First Approach**

#### Step 1: Design API in SwaggerHub
1. Create new API in SwaggerHub
2. Use visual editor to design endpoints
3. Define schemas, parameters, responses
4. Add examples and descriptions

#### Step 2: Generate FastAPI Code
```bash
# SwaggerHub can generate FastAPI code from your spec
# Download generated code and integrate with your project
```

#### Step 3: Sync Changes
- Update your FastAPI code to match SwaggerHub spec
- Or update SwaggerHub spec to match your code

### 3. **Continuous Integration**

#### GitHub Actions Workflow
```yaml
# .github/workflows/api-sync.yml
name: API Specification Sync

on:
  push:
    branches: [main]
    paths: ['web_server.py']

jobs:
  sync-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install fastapi uvicorn
      
      - name: Start server and export spec
        run: |
          python web_server.py &
          sleep 10
          curl http://localhost:8000/openapi.json > api-spec.json
      
      - name: Upload to SwaggerHub
        uses: swaggerhub/upload-api@v1
        with:
          api: your-org/your-api-name
          version: ${{ github.sha }}
          file: api-spec.json
          token: ${{ secrets.SWAGGERHUB_TOKEN }}
```

## Enhanced FastAPI Configuration

### 1. **Improved OpenAPI Metadata**

Update your `web_server.py` for better SwaggerHub integration:

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="LPL-MCP Web Server",
        version="1.0.0",
        description="""
        ## LPL-MCP Web Server API
        
        A comprehensive FastAPI web server with user management, health monitoring, and analytics.
        
        ### Features
        * **User Management**: Complete CRUD operations
        * **Health Monitoring**: System status and uptime
        * **Analytics**: Usage statistics and metrics
        * **Authentication**: JWT-based security (planned)
        
        ### Getting Started
        1. Create a user using POST /users
        2. Retrieve users with GET /users
        3. Monitor system health with GET /health
        4. View analytics with GET /analytics
        """,
        routes=app.routes,
        tags=[
            {"name": "users", "description": "User management operations"},
            {"name": "health", "description": "System health and monitoring"},
            {"name": "analytics", "description": "System analytics and metrics"},
        ]
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### 2. **Add API Tags and Examples**

```python
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional

# Enhanced User model with examples
class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="User's full name",
        example="John Doe"
    )
    email: str = Field(
        ..., 
        description="User's email address",
        example="john.doe@example.com"
    )
    age: Optional[int] = Field(
        None, 
        ge=0, 
        le=150, 
        description="User's age",
        example=30
    )
    is_active: bool = Field(
        True, 
        description="Whether the user is active",
        example=True
    )

# Tagged endpoints
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
async def create_user(user: User):
    """Create a new user in the system"""
    # ... implementation

@app.get("/users", response_model=List[UserResponse], tags=["users"])
async def get_users(skip: int = 0, limit: int = 100):
    """Retrieve all users with pagination support"""
    # ... implementation

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Check system health and status"""
    # ... implementation

@app.get("/analytics", tags=["analytics"])
async def get_analytics():
    """Get system analytics and metrics"""
    # ... implementation
```

## SwaggerHub Best Practices

### 1. **API Versioning**
```python
# In your FastAPI app
app = FastAPI(
    title="LPL-MCP Web Server",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)
```

### 2. **Environment-Specific Configurations**
```python
import os

# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    app = FastAPI(
        title="LPL-MCP Web Server",
        version="1.0.0",
        docs_url=None,  # Disable docs in production
        redoc_url=None
    )
else:
    app = FastAPI(
        title="LPL-MCP Web Server (Development)",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
```

### 3. **API Documentation Standards**
```python
# Comprehensive endpoint documentation
@app.post(
    "/users", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Create User",
    description="""
    Create a new user in the system.
    
    - **name**: User's full name (required)
    - **email**: User's email address (required, must be unique)
    - **age**: User's age (optional, 0-150)
    - **is_active**: Whether the user is active (default: true)
    
    Returns the created user with assigned ID and timestamp.
    """,
    response_description="User successfully created",
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
                        "created_at": "2024-01-01T12:00:00"
                    }
                }
            }
        },
        400: {
            "description": "Bad request - email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered",
                        "timestamp": "2024-01-01T12:00:00"
                    }
                }
            }
        }
    }
)
async def create_user(user: User):
    # ... implementation
```

## SwaggerHub Features for Your Project

### 1. **API Mocking**
- Generate mock servers from your API spec
- Test frontend integration without backend
- Validate API contracts

### 2. **Code Generation**
- Generate client SDKs in multiple languages
- Create server stubs
- Generate TypeScript interfaces

### 3. **API Testing**
- Built-in test runner
- Automated API validation
- Performance testing

### 4. **Team Collaboration**
- Comment on API changes
- Review and approve modifications
- Track API evolution

## Integration Checklist

- [ ] Export current OpenAPI spec from FastAPI
- [ ] Import to SwaggerHub
- [ ] Configure team access and permissions
- [ ] Set up CI/CD pipeline for automatic sync
- [ ] Add comprehensive examples and descriptions
- [ ] Implement API versioning strategy
- [ ] Configure environment-specific settings
- [ ] Set up automated testing
- [ ] Document API standards and guidelines

## Next Steps

1. **Sign up for SwaggerHub** at https://swaggerhub.com
2. **Export your current API** specification
3. **Import to SwaggerHub** and explore the platform
4. **Enhance your FastAPI code** with better documentation
5. **Set up CI/CD integration** for automated sync
6. **Invite team members** for collaboration

## Resources

- [SwaggerHub Documentation](https://support.smartbear.com/swaggerhub/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [API Design Best Practices](https://swagger.io/blog/api-design/) 