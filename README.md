# LPL-MCP Project

## Overview
LPL-MCP is a modular project designed to demonstrate integration between Jira, PostgreSQL, MySQL, and a Python-based web server. It provides a foundation for managing, tracking, and visualizing project data using modern DevOps and data engineering practices.

## Main Components

- **Jira (Atlassian)**: Issue and project tracking, running in a Docker container.
- **PostgreSQL**: Relational database for Jira data, running in a Docker container.
- **MySQL**: Additional relational database for custom data storage, running in a Docker container.
- **WebServer**: Python FastAPI application for exposing REST APIs, running in a Docker container.
- **MCP Integration**: Configuration for connecting to Jira, Postgres, and MySQL using MCP (Multi-Cloud Platform) tools.

## Project Structure

```
LPL-MCP/
├── Repository/
│   ├── docker-compose.yaml         # Orchestrates Jira, Postgres, MySQL
│   └── WebServer/                 # FastAPI web server and Dockerfile
│       ├── web_server.py
│       ├── web_server_enhanced.py
│       ├── requirements.txt
│       └── ...
├── .gitignore                     # Ignores node_modules and other files
├── README.md                      # Project documentation
└── ...
```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repo-url>
cd LPL-MCP
```

### 2. Start Core Services (Jira, Postgres, MySQL)
```sh
cd Repository
docker-compose up -d
```

### 3. Build and Run the Web Server
```sh
cd Repository/WebServer
# Build the Docker image
docker build -t webserver:latest .
# Run the container
docker run -d -p 8000:8000 --name webserver webserver:latest
```

### 4. Access the Web Server
- API: [http://localhost:8000](http://localhost:8000)
- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 5. MCP Configuration
- The `.cursor/mcp.json` file contains connection details for Jira, Postgres, and MySQL.
- Update credentials and host addresses as needed for your environment.

## Usage
- Use Jira for project and issue tracking.
- Use the web server's REST API to interact with user and analytics endpoints.
- Data is stored in PostgreSQL (for Jira) and MySQL (for custom tables).
- The project demonstrates syncing Jira ticket status to MySQL and exposing analytics via API.

## Development
- Python code is in `Repository/WebServer/`.
- Update or add endpoints in `web_server_enhanced.py`.
- Use `requirements.txt` to manage Python dependencies.

## Notes
- Ensure Docker is installed and running on your system.
- Default credentials and ports are for local development; change them for production use.
- The project is modular and can be extended for additional integrations.

## License
MIT License