@echo off
REM hidemenot Challenge Platform Startup Script (Windows)
REM Author: Challenge Developer
REM Description: Easy startup script for the hidemenot steganography challenge

echo 🔐 hidemenot Challenge Platform
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip is available

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies. Try running manually:
        echo    pip install -r requirements.txt
        pause
        exit /b 1
    )
    
    echo ✅ Dependencies installed successfully
) else (
    echo ⚠️  requirements.txt not found. Installing dependencies manually...
    pip install Flask Flask-Login Pillow Werkzeug bcrypt
)

REM Create necessary directories
echo 📁 Setting up directories...
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\images" mkdir "static\images"
if not exist "adminrandomhashorlongtexttopreventguess\logs" mkdir "adminrandomhashorlongtexttopreventguess\logs"

echo ✅ Directories created

REM Check if app.py exists
if not exist "app.py" (
    echo ❌ app.py not found. Make sure you're in the correct directory.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting hidemenot application...
echo 📱 Access URL: http://localhost:5000
echo ⏹️  Press Ctrl+C to stop the server
echo.
echo 🎯 Challenge Instructions:
echo 1. Register an account and explore the steganography features
echo 2. Try uploading polyglot files to trigger interesting behavior
echo 3. Check page source code for hidden clues
echo 4. Use timing and HTTP header manipulation for advanced stages
echo.
echo 💡 Need help? Check README.md for detailed walkthrough
echo 🔧 Testing tools available: create_polyglot.py, test_exploit.py
echo.

REM Start the Flask application
python ./app.py

pause
