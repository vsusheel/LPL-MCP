#!/bin/bash

# LPL-MCP FastAPI Web Server Startup Script

echo "🚀 Starting LPL-MCP FastAPI Web Server..."
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "web_server.py" ]; then
    echo "❌ web_server.py not found. Please run this script from the WebServer directory."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure all files are present."
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check your Python environment."
        exit 1
    fi
fi

# Set environment variables
export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}

echo "🌐 Server will start on http://$HOST:$PORT"
echo "📚 API Documentation will be available at:"
echo "   - Interactive docs: http://$HOST:$PORT/docs"
echo "   - ReDoc: http://$HOST:$PORT/redoc"
echo "🏥 Health check: http://$HOST:$PORT/health"
echo ""

# Start the server
echo "▶️  Starting server..."
python3 web_server.py 