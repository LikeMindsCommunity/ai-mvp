# Use Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p projects

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"] 