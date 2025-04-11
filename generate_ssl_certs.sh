#!/bin/bash

# Script to generate self-signed SSL certificates for the Flutter Integration Assistant

# Set variables
SSL_DIR="./ssl"
CERT_FILE="$SSL_DIR/cert.pem"
KEY_FILE="$SSL_DIR/key.pem"
DOMAIN="localhost"
IP="98.70.88.101"  # Replace with your public IP if needed

# Create SSL directory if it doesn't exist
mkdir -p $SSL_DIR

echo "Generating self-signed SSL certificates for $DOMAIN and IP $IP..."

# Generate self-signed certificate valid for one year (365 days)
openssl req -x509 -newkey rsa:4096 -keyout $KEY_FILE -out $CERT_FILE -sha256 -days 365 -nodes \
    -subj "/CN=$DOMAIN" \
    -addext "subjectAltName = DNS:$DOMAIN,IP:$IP,IP:127.0.0.1"

# Check if certificates were created successfully
if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "SSL certificates generated successfully."
    echo "Certificate: $CERT_FILE"
    echo "Private key: $KEY_FILE"
    
    # Set appropriate permissions
    chmod 644 $CERT_FILE
    chmod 600 $KEY_FILE
    
    echo "To use these certificates with Docker, run:"
    echo "docker-compose up --build"
else
    echo "Failed to generate SSL certificates."
    exit 1
fi

echo "Done." 