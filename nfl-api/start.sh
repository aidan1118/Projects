#!/bin/bash

# NFL API Launch Script
echo "🏈 Starting NFL Data API..."

# Detect Python command
PYTHON_CMD=""
if command -v python3 > /dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python > /dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.7+"
    exit 1
fi

# Detect pip command
PIP_CMD=""
if command -v pip3 > /dev/null 2>&1; then
    PIP_CMD="pip3"
elif command -v pip > /dev/null 2>&1; then
    PIP_CMD="pip"
else
    echo "❌ pip not found. Please install pip"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Verify activation worked by checking for the right python
if [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
    PIP_CMD="venv/bin/pip"
else
    echo "⚠️  Virtual environment activation may have failed, continuing with system Python"
fi

# Install/update requirements
echo "⬇️  Installing dependencies..."
$PIP_CMD install -q -r requirements.txt

# Kill any existing process on port 5001
echo "🔄 Checking for existing server..."
if command -v lsof > /dev/null 2>&1; then
    if lsof -ti:5001 > /dev/null 2>&1; then
        echo "⚠️  Stopping existing server on port 5001..."
        lsof -ti:5001 | xargs kill -9 2>/dev/null
        sleep 2
    fi
elif command -v netstat > /dev/null 2>&1; then
    # Alternative check for Windows/systems without lsof
    if netstat -an | grep :5001 > /dev/null 2>&1; then
        echo "⚠️  Port 5001 appears to be in use. You may need to stop existing processes manually."
    fi
fi

# Start the server
echo "🚀 Starting NFL API on http://localhost:5001"
echo "📊 Available endpoints:"
echo "   • http://localhost:5001/ (API info)"
echo "   • http://localhost:5001/nfl/games"
echo "   • http://localhost:5001/nfl/stats"
echo "   • http://localhost:5001/nfl/teams"
echo "   • http://localhost:5001/nfl/bye-weeks"
echo "   • http://localhost:5001/nfl/team-performance"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

# Run the app with the correct Python command
$PYTHON_CMD app.py