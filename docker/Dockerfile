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

# Run flutter doctor and accept licenses
RUN flutter doctor
RUN yes | flutter doctor --android-licenses || true

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the API port
EXPOSE 8000

# Command to run the server
CMD ["python", "run_server.py"] 