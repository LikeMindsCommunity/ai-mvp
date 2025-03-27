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
python run_api.py &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started with PID ${BACKEND_PID}${NC}"

# Wait for backend to start
echo "Waiting for backend to initialize (5 seconds)..."
sleep 5

# Start frontend development server
echo -e "${GREEN}Starting frontend development server...${NC}"
cd frontend

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
    <!-- Google Fonts - Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
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
    
    # Create basic CSS file if it doesn't exist
    mkdir -p src
    if [ ! -f "src/index.css" ]; then
        cat > src/index.css << EOL
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;

    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;

    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;

    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;

    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;

    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;

    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;

    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;

    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;

    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;

    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
EOL
    fi
    
    # Create lib directory and utils
    mkdir -p src/lib
    cat > src/lib/utils.ts << EOL
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
EOL
    
    echo -e "${GREEN}Frontend files created successfully.${NC}"
fi

# Install necessary dependencies
echo -e "${YELLOW}Installing necessary dependencies...${NC}"
npm install -s tailwind-merge clsx class-variance-authority 2>/dev/null

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