#!/bin/bash

# hidemenot Challenge Platform Startup Script
# Author: Challenge Developer
# Description: Easy startup script for the hidemenot steganography challenge

echo "🔐 hidemenot Challenge Platform"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Use pip3 if available, otherwise pip
PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✅ Using $PIP_CMD for package management"

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    $PIP_CMD install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Try running manually:"
        echo "   $PIP_CMD install -r requirements.txt"
        exit 1
    fi
    
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  requirements.txt not found. Installing dependencies manually..."
    $PIP_CMD install Flask Flask-Login Pillow Werkzeug bcrypt
fi

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p static/uploads
mkdir -p static/images
mkdir -p adminrandomhashorlongtexttopreventguess/logs

echo "✅ Directories created"

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Make sure you're in the correct directory."
    exit 1
fi

echo ""
echo "🚀 Starting hidemenot application..."
echo "📱 Access URL: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""
echo "🎯 Challenge Instructions:"
echo "1. Register an account and explore the steganography features"
echo "2. Try uploading polyglot files to trigger interesting behavior"
echo "3. Check page source code for hidden clues"
echo "4. Use timing and HTTP header manipulation for advanced stages"
echo ""
echo "💡 Need help? Check README.md for detailed walkthrough"
echo "🔧 Testing tools available: create_polyglot.py, test_exploit.py"
echo ""

# Start the Flask application
python3 app.py
