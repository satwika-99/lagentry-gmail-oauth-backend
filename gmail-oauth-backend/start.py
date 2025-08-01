#!/usr/bin/env python3
"""
Startup script for Gmail OAuth Backend
"""

import sys
import os
from config import config

def main():
    """Start the Gmail OAuth Backend server"""
    print(" Gmail OAuth Backend")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print(" Error: main.py not found in current directory")
        print(" Make sure you're in the app directory")
        sys.exit(1)
    
    # Validate configuration
    print(" Validating configuration...")
    if not config.validate():
        print("\n Configuration validation failed!")
        print("\n Required environment variables:")
        print("  GOOGLE_CLIENT_ID - Your Google OAuth Client ID")
        print("  GOOGLE_CLIENT_SECRET - Your Google OAuth Client Secret")
        print("\n Create a .env file with these variables:")
        print("  GOOGLE_CLIENT_ID=your_client_id_here")
        print("  GOOGLE_CLIENT_SECRET=your_client_secret_here")
        print("  REDIRECT_URI=http://localhost:8000/auth/google/callback")
        sys.exit(1)
    
    # Print configuration summary
    config.print_config()
    
    print(f"\n Starting server on http://{config.HOST}:{config.PORT}")
    print(" API Documentation: http://localhost:8000/docs")
    print(" OAuth Flow: http://localhost:8000/auth/google")
    print("\n Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Import and run the main application
    try:
        from main import app
        import uvicorn
        
        uvicorn.run(
            app, 
            host=config.HOST, 
            port=config.PORT,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n Server stopped by user")
    except Exception as e:
        print(f"\n Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
