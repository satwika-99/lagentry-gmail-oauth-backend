#!/usr/bin/env python3
"""
Startup script for Lagentry OAuth Backend
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def main():
    """Main startup function"""
    print("🚀 Starting Lagentry OAuth Backend...")
    
    # Set default environment variables if not already set
    os.environ.setdefault('HOST', '127.0.0.1')
    os.environ.setdefault('PORT', '8081')
    os.environ.setdefault('DEBUG', 'true')
    os.environ.setdefault('DATABASE_PATH', 'oauth_tokens.db')
    
    # Load environment variables from .env file if it exists
    env_file = app_dir / '.env'
    if env_file.exists():
        print(f"📁 Loading environment from: {env_file}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # Get configuration from environment
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 8081))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    log_level = os.getenv('LOG_LEVEL', 'INFO').lower()
    
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print(f"📝 Log level: {log_level}")
    print("=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=debug,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
