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

### WebSocket API

The API provides a WebSocket interface for real-time updates during project compilation and preview.

#### WebSocket Endpoint

- `WebSocket /ws/{project_id}`: WebSocket endpoint for real-time project updates

#### Connection Flow

1. Connect to the WebSocket endpoint with a valid project ID
2. On successful connection, you'll receive a "connected" status message
3. Send a "compile" message to request compilation
4. Receive real-time updates during the compilation process
5. Receive a completion message with success status when done

#### Message Types

The WebSocket API uses JSON messages with the following format:

```json
{
  "type": "status|error|preview|completion",
  "data": {
    // Type-specific data
  },
  "timestamp": "ISO date string"
}
```

**Message Types:**

1. **Status Messages** (type: "status")
   ```json
   {
     "type": "status",
     "data": {
       "status": "connected|compiling|completed",
       "details": {}
     },
     "timestamp": "2025-04-10T10:30:00.000Z"
   }
   ```

2. **Error Messages** (type: "error")
   ```json
   {
     "type": "error",
     "data": {
       "error": "Error message"
     },
     "timestamp": "2025-04-10T10:30:00.000Z"
   }
   ```

3. **Preview Updates** (type: "preview")
   ```json
   {
     "type": "preview",
     "data": {
       "url": "/preview/project-id"
     },
     "timestamp": "2025-04-10T10:30:00.000Z"
   }
   ```

4. **Completion Messages** (type: "completion")
   ```json
   {
     "type": "completion",
     "data": {
       "success": true,
       "details": {}
     },
     "timestamp": "2025-04-10T10:30:00.000Z"
   }
   ```

#### WebSocket Example (JavaScript)

```javascript
// Connect to the WebSocket
const socket = new WebSocket(`ws://localhost:8001/ws/${projectId}`);

// Handle connection open
socket.onopen = () => {
  console.log("WebSocket connection established");
};

// Handle incoming messages
socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(`Received ${message.type} message:`, message.data);
  
  // Handle different message types
  switch (message.type) {
    case "status":
      // Update UI with status
      break;
    case "error":
      // Display error
      break;
    case "preview":
      // Update preview iframe
      document.getElementById("preview").src = message.data.url;
      break;
    case "completion":
      // Handle completion
      break;
  }
};

// Request compilation
function requestCompile() {
  socket.send("compile");
}
```

## Testing

### Testing API Health

Use the basic test script to verify API functionality:

```bash
python test_api.py
```

### Testing WebSocket Functionality

To test the WebSocket functionality:

```bash
# Test with a specific project ID
python test_websocket.py --project-id YOUR_PROJECT_ID

# Full integration test (creates project and tests WebSocket)
python test_websocket_integration.py
```

You can also use the provided HTML test page:
1. Open `websocket_test.html` in a browser
2. Enter a project ID or use the default one
3. Click "Check Project" to verify the project exists
4. Click "Connect" to establish a WebSocket connection
5. Once connected, click "Send Compile Command" to test the compilation flow

## Troubleshooting

### Port Conflicts

If you see "Connection reset by peer" errors, there may be another service using port 8000. The API now runs on port 8001 by default to avoid this issue.

### Docker Connection Issues

If you see timeout errors or Docker-related errors:

1. Check if Docker is running: `docker info`
2. Restart Docker if needed
3. The API will fall back to a basic functionality mode if Docker is not available

### WebSocket Connection Issues

If you're having issues with WebSocket connections:

1. Verify the project ID exists using the debug endpoint: `GET /debug/project/{project_id}`
2. Check for any network restrictions that might block WebSocket connections
3. Try different hostnames (localhost, 127.0.0.1) if connections are failing

## License

[Your license information here] 