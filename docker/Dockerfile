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

# Copy only necessary files for the application
COPY *.py *.txt ./
COPY api/ ./api/
COPY flutter_generator/ ./flutter_generator/
COPY integration/ ./integration/
# Make sure .dockerignore excludes unnecessary files

# Expose the API port
EXPOSE 8000

# Command to run the server
CMD ["python", "run_server.py"] 