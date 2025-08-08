#!/usr/bin/env python3
"""
Simple server startup script for the Lagentry OAuth Backend
"""

import uvicorn
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the OAuth backend server"""
    
    print("🚀 Starting Lagentry OAuth Backend Server...")
    print("🌐 Server will be available at: http://127.0.0.1:8083")
    print("📚 API Documentation: http://127.0.0.1:8083/docs")
    print("=" * 50)
    
    try:
        # Run the server using uvicorn
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8083,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
