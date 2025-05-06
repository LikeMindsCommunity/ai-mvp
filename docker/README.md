# Docker Setup for Flutter Integration Assistant

This directory contains Docker files to run the Flutter Integration Assistant in a containerized environment.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Copy the example environment file and add your Google API key:

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

2. Build and start the containers:

```bash
cd docker
docker-compose up -d
```

3. The API will be available at:
   - WebSocket endpoint: `ws://localhost:8000/api/flutter`
   - Health check: `http://localhost:8000/`

4. Generated Flutter web previews will be available at:
   - `http://localhost:8080/`

## Stopping the Service

```bash
docker-compose down
```

## Viewing Logs

```bash
docker-compose logs -f
```

## Rebuilding After Changes

```bash
docker-compose down
docker-compose build
docker-compose up -d
``` 