#!/usr/bin/env python3
"""
Simple server startup script for Gmail OAuth Backend
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting Gmail OAuth Backend...")
    print("Server will be available at: http://127.0.0.1:8005")
    print("API Documentation: http://127.0.0.1:8005/docs")
    print("OAuth Flow: http://127.0.0.1:8005/auth/google")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8005, 
        log_level="info",
        reload=False
    ) 