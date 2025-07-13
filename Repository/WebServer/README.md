# LPL-MCP FastAPI Web Server

A modern, production-ready FastAPI web server with comprehensive features including user management, health monitoring, and analytics.

## Features

- 🚀 **FastAPI Framework** - High-performance async web framework
- 📚 **Auto-generated Documentation** - Interactive API docs at `/docs` and `/redoc`
- 🔒 **Input Validation** - Pydantic models for request/response validation
- 🌐 **CORS Support** - Cross-origin resource sharing enabled
- 📊 **Health Monitoring** - Built-in health check endpoint
- 👥 **User Management** - Complete CRUD operations for users
- 📈 **Analytics** - Basic system analytics
- 🐳 **Docker Support** - Containerized deployment
- 🔍 **Logging** - Comprehensive logging system
- ⚡ **Async/Await** - Non-blocking I/O operations

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)

### Local Development

1. **Clone and navigate to the project:**
   ```bash
   cd LPL-MCP/Repository/WebServer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python web_server.py
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually:**
   ```bash
   docker build -t lpl-mcp-web-server .
   docker run -p 8000:8000 lpl-mcp-web-server
   ```

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check and system status |
| GET | `/analytics` | System analytics |

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a new user |
| GET | `/users` | Get all users (with pagination) |
| GET | `/users/{user_id}` | Get specific user |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

## Request/Response Examples

### Create User
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30,
       "is_active": true
     }'
```

### Get All Users
```bash
curl -X GET "http://localhost:8000/users?skip=0&limit=10"
```

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

## Data Models

### User Model
```python
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "is_active": true,
  "created_at": "2024-01-01T12:00:00"
}
```

### Health Check Response
```python
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0",
  "uptime": 3600.0
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `PYTHONPATH` | /app | Python path |

## Development

### Project Structure
```
WebServer/
├── web_server.py      # Main FastAPI application
├── requirements.txt   # Python dependencies
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose setup
└── README.md         # This file
```

### Adding New Endpoints

1. Define Pydantic models for request/response validation
2. Create the endpoint function with proper decorators
3. Add error handling and logging
4. Update this README with endpoint documentation

### Testing

The server includes comprehensive error handling and validation. Test the endpoints using:

- Interactive documentation at `/docs`
- curl commands
- Postman or similar API testing tools

## Production Considerations

### Security
- Configure CORS origins properly for production
- Implement proper authentication and authorization
- Use environment variables for sensitive data
- Enable HTTPS in production

### Performance
- Replace in-memory storage with a proper database
- Implement caching strategies
- Add rate limiting
- Monitor performance metrics

### Monitoring
- Health check endpoint for load balancers
- Structured logging for monitoring systems
- Metrics collection
- Error tracking

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port in environment variable
   PORT=8001 python web_server.py
   ```

2. **Docker build fails:**
   ```bash
   # Clean Docker cache
   docker system prune -a
   ```

3. **Import errors:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

## Contributing

1. Follow PEP 8 style guidelines
2. Add proper docstrings to functions
3. Include error handling
4. Update documentation
5. Test your changes

## License

This project is part of the LPL-MCP learning repository. 