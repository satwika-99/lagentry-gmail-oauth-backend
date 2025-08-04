#!/usr/bin/env python3
"""
Startup script for the Gmail OAuth Backend
"""

import subprocess
import sys
import os

def main():
    """Start the Gmail OAuth backend server"""
    
    # Change to the app directory
    app_dir = os.path.join(os.path.dirname(__file__), 'app')
    os.chdir(app_dir)
    
    print("🚀 Starting Gmail OAuth Backend Server...")
    print(f"📁 Working directory: {os.getcwd()}")
    print("🌐 Server will be available at: http://127.0.0.1:8080")
    print("📚 API Documentation: http://127.0.0.1:8080/docs")
    print("=" * 50)
    
    try:
        # Run the main server
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 