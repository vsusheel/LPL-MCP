# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and source code
COPY inventory_api.py /app/inventory_api.py
COPY test_inventory_api.py /app/test_inventory_api.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest pytest-cov

# Expose port
EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "inventory_api:app", "--host", "0.0.0.0", "--port", "8000"] 