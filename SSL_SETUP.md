# Setting up SSL for WebSocket Communication

This guide explains how to set up SSL support for secure WebSocket communications (WSS) with the Flutter Integration Assistant.

## Prerequisites

- OpenSSL installed on your system
- Docker and Docker Compose (if running in Docker)

## Generating SSL Certificates

1. Run the certificate generation script:

   ```bash
   ./generate_ssl_certs.sh
   ```

   This will:
   - Create a `ssl` directory if it doesn't exist
   - Generate a self-signed SSL certificate and private key
   - Set appropriate permissions

2. The generated files will be:
   - `ssl/cert.pem` - SSL certificate
   - `ssl/key.pem` - Private key

## Configuration

### Environment Variables

The following environment variables control SSL behavior:

- `ENABLE_SSL`: Set to `true` to enable SSL (default: `false`)
- `SSL_CERT_FILE`: Path to the SSL certificate (default: `/app/ssl/cert.pem`)
- `SSL_KEY_FILE`: Path to the SSL private key (default: `/app/ssl/key.pem`)
- `SSL_PORT`: Port for HTTPS/WSS connections (default: `8443`)
- `API_PORT`: Port for HTTP/WS connections (default: `8000`)

### Docker Setup

1. Copy the example environment file:

   ```bash
   cp docker-compose.env.example .env
   ```

2. Edit the `.env` file to adjust your settings if needed.

3. Start the Docker container:

   ```bash
   docker-compose up --build
   ```

### Direct Setup (No Docker)

If running without Docker:

1. Generate SSL certificates as described above
2. Set the environment variables:

   ```bash
   export ENABLE_SSL=true
   export SSL_CERT_FILE="./ssl/cert.pem"
   export SSL_KEY_FILE="./ssl/key.pem" 
   export SSL_PORT=8443
   export API_PORT=8000
   ```

3. Run the server:

   ```bash
   python run_server.py
   ```

## Testing the WebSocket Connection

1. Open the WebSocket tester in your browser:
   - Secure connection: `https://localhost:8443/websocket-tester`
   - Non-secure connection: `http://localhost:8000/websocket-tester`

2. In the tester UI:
   - Select the appropriate protocol (`ws://` or `wss://`)
   - Set the hostname (e.g., `localhost`)
   - Set the port (`8000` for ws:// or `8443` for wss://`)
   - Enter the endpoint (`/api/flutter`)
   - Click "Connect"

## Browser Security Considerations

When using self-signed certificates, your browser may show security warnings. For testing purposes, you can:

1. In Chrome: Click "Advanced" and then "Proceed to localhost (unsafe)"
2. Or access `chrome://flags/#allow-insecure-localhost` and enable it

For production, use properly signed certificates from a trusted certificate authority. 