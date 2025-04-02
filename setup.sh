#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting setup..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create and activate virtual environment
echo "🔧 Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate virtual environment (works for both bash and zsh)
source .venv/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# Install requirements
echo "📦 Installing requirements..."
pip install google.generativeai python-dotenv

# Check if .env file exists, if not create it with a placeholder
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "GOOGLE_API_KEY=your_api_key_here" > .env
    echo "⚠️ Please update the GOOGLE_API_KEY in .env file with your actual API key"
fi

# Check if docs directory exists
if [ ! -d "docs" ]; then
    echo "❌ docs directory not found. Please make sure it exists and contains the required documentation."
    exit 1
fi

# Run the application
echo "🏃 Running the application..."
python3 google.py

echo "✅ Setup complete!" 