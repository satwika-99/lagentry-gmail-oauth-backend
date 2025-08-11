@echo off
REM Lagentry OAuth Backend Deployment Script for Windows

echo 🚀 Deploying Lagentry OAuth Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python version: %PYTHON_VERSION%

REM Check if virtual environment exists
if not exist "venv" (
    echo 📁 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️ .env file not found. Please create one with your OAuth credentials.
    echo 📝 You can copy from .env.example and update the values.
)

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Test the backend
echo 🧪 Testing backend...
python test_backend.py

if %errorlevel% equ 0 (
    echo ✅ Backend is ready!
    echo.
    echo 🌐 To start the backend, run:
    echo    python start_backend.py
    echo.
    echo 📚 API documentation will be available at:
    echo    http://127.0.0.1:8081/docs
    echo.
    echo 🔍 Health check:
    echo    http://127.0.0.1:8081/health
) else (
    echo ❌ Backend test failed. Please check the configuration.
    pause
    exit /b 1
)

echo.
echo ✅ Deployment completed successfully! 🎉
pause
