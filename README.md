# LikeMinds Flutter Integration Assistant API

This API provides services for generating and previewing Flutter code for integration with LikeMinds SDKs.

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Running the Server

Use the provided script to start the server:

```bash
./start_server.sh
```

This will start the server on port 8001 to avoid conflicts with Docker. The server will be available at http://localhost:8001.

### Important Note About Docker

The API uses Docker for Flutter project creation and compilation, but has a fallback mechanism if Docker is not available or not responding. If you want full functionality:

1. Make sure Docker is installed and running
2. Ensure the user running the API has permission to use Docker

## API Endpoints

### Root Endpoint

- `GET /`: Basic information about the API

### Test Endpoint

- `GET /api/v1/test`: Simple test endpoint to verify API functionality without external dependencies

### Code Generation

- `POST /api/v1/generate`: Generate Flutter code based on a prompt
  - Request:
    ```json
    {
      "prompt": "Create a simple Flutter app with a chat interface",
      "project_id": null
    }
    ```
  - Response:
    ```json
    {
      "success": true,
      "code": "// Generated Flutter code",
      "project_id": "generated-uuid"
    }
    ```

### WebSocket Preview

- `WebSocket /ws/{project_id}`: WebSocket endpoint for real-time project updates

## Troubleshooting

### Port Conflicts

If you see "Connection reset by peer" errors, there may be another service using port 8000. The API now runs on port 8001 by default to avoid this issue.

### Docker Connection Issues

If you see timeout errors or Docker-related errors:

1. Check if Docker is running: `docker info`
2. Restart Docker if needed
3. The API will fall back to a basic functionality mode if Docker is not available

### Testing API Health

Use the test script to verify API functionality:

```bash
python test_api.py
```

## License

[Your license information here] 