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
COPY ssl/ ./ssl/


# Set environment variables
ENV WEB_HOST=0.0.0.0
ENV PUBLIC_HOST=98.70.88.101
ENV FLUTTER_WEB_PORT=8080
ENV API_PORT=8000
ENV SSL_PORT=8443

# Expose ports
EXPOSE 8000 8080 8443

# Command to run the server
CMD ["python", "run_server.py"] 