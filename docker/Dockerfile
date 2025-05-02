FROM python:3.11-slim

WORKDIR /app

# Install Flutter SDK
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Download and setup Flutter
RUN git clone https://github.com/flutter/flutter.git -b stable /flutter
ENV PATH="/flutter/bin:${PATH}"

# Run flutter doctor
RUN flutter doctor
RUN yes | flutter doctor --android-licenses || true

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install watchfiles for Uvicorn hot reload
RUN pip install --no-cache-dir watchfiles

# Copy only necessary files for the application
COPY *.py *.txt ./
COPY api/ ./api/
COPY flutter_generator/ ./flutter_generator/
COPY integration/ ./integration/

# Environment variables will be loaded from .env file at runtime
# These are just default values that can be overridden
ENV WEB_HOST=${WEB_HOST:-0.0.0.0}
ENV PUBLIC_HOST=${PUBLIC_HOST:-localhost}
ENV FLUTTER_WEB_PORT=${FLUTTER_WEB_PORT:-8080}
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY:-}
ENV API_URL=${API_URL:-http://localhost:8000}
ENV GITHUB_APP_ID=${GITHUB_APP_ID:-}
ENV GITHUB_APP_NAME=${GITHUB_APP_NAME:-}
ENV GITHUB_APP_CLIENT_ID=${GITHUB_APP_CLIENT_ID:-}
ENV GITHUB_APP_CLIENT_SECRET=${GITHUB_APP_CLIENT_SECRET:-}
ENV GITHUB_APP_PRIVATE_KEY_PATH=${GITHUB_APP_PRIVATE_KEY_PATH:-}

# Make sure .dockerignore excludes unnecessary files

# Expose the API port
EXPOSE 8000 8080

# Command to run the server
CMD ["python", "run_server.py"] 