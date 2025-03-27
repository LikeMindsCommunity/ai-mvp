FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port
EXPOSE $PORT

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 