#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Starting LikeMinds Documentation Assistant ===${NC}"
echo

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found in the root directory.${NC}"
    echo "Creating a sample .env file. Please edit it with your actual API keys."
    
    # Create a sample .env file
    cat > .env << EOL
# API Keys for LLM services
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Model configurations
EMBEDDING_MODEL=text-embedding-3-large
QUERY_MODEL=claude-3-7-sonnet-20250219
CONTEXT_MODEL=gpt-4o
RESPONSE_MODEL=claude-3-7-sonnet-20250219

# API settings
HOST=0.0.0.0
PORT=8000
EOL
    
    echo "Sample .env file created. Please edit it before continuing."
    exit 1
fi

# Check and create frontend .env if needed
if [ ! -f "frontend/.env" ]; then
    echo -e "${YELLOW}Creating frontend .env file...${NC}"
    echo "VITE_API_URL=http://localhost:8000/api" > frontend/.env
    echo -e "${GREEN}Frontend .env file created.${NC}"
fi

# Start backend server
echo -e "${GREEN}Starting backend server...${NC}"
cd backend
python -m app.main &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started with PID ${BACKEND_PID}${NC}"

# Wait for backend to start
echo "Waiting for backend to initialize (5 seconds)..."
sleep 5

# Start frontend development server
echo -e "${GREEN}Starting frontend development server...${NC}"
cd ../frontend

# Check if index.html exists
if [ ! -f "index.html" ]; then
    echo -e "${YELLOW}Creating necessary frontend files...${NC}"
    
    # Create index.html if it doesn't exist
    cat > index.html << EOL
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LikeMinds Documentation Assistant</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOL
    
    # Create public directory and favicon if they don't exist
    mkdir -p public
    cat > public/favicon.svg << EOL
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10" fill="#4299E1" />
  <path d="M8 12h8M12 8v8" stroke="white" />
</svg>
EOL
    
    echo -e "${GREEN}Frontend files created successfully.${NC}"
fi

npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend server started with PID ${FRONTEND_PID}${NC}"

echo
echo -e "${BLUE}=== Services Running ===${NC}"
echo -e "Backend: ${GREEN}http://localhost:8000${NC}"
echo -e "Frontend: ${GREEN}http://localhost:3000${NC}"
echo
echo -e "${BLUE}=== Press Ctrl+C to stop both servers ===${NC}"

# Function to kill processes on exit
function cleanup {
    echo
    echo -e "${BLUE}Shutting down servers...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    echo -e "${GREEN}Servers stopped successfully.${NC}"
    exit 0
}

# Register the cleanup function for when Ctrl+C is pressed
trap cleanup INT

# Wait for user to press Ctrl+C
wait 