#!/bin/bash

# Lagentry OAuth Backend Deployment Script

set -e

echo "🚀 Deploying Lagentry OAuth Backend..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

print_status "Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Please create one with your OAuth credentials."
    print_status "You can copy from .env.example and update the values."
fi

# Create data directory if it doesn't exist
mkdir -p data

# Test the backend
print_status "Testing backend..."
python test_backend.py

if [ $? -eq 0 ]; then
    print_status "✅ Backend is ready!"
    echo ""
    echo "🌐 To start the backend, run:"
    echo "   python start_backend.py"
    echo ""
    echo "📚 API documentation will be available at:"
    echo "   http://127.0.0.1:8081/docs"
    echo ""
    echo "🔍 Health check:"
    echo "   http://127.0.0.1:8081/health"
else
    print_error "❌ Backend test failed. Please check the configuration."
    exit 1
fi

echo ""
print_status "Deployment completed successfully! 🎉"
