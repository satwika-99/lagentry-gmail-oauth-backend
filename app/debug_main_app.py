#!/usr/bin/env python3

print("=== Debugging Main App ===")

try:
    print("1. Importing config...")
    from config import config
    print("   ✓ Config imported")
    
    print("2. Initializing database...")
    from storage import init_db
    init_db()
    print("   ✓ Database initialized")
    
    print("3. Testing auth imports...")
    from auth import generate_auth_url
    print("   ✓ Auth imported")
    
    print("4. Testing gmail imports...")
    from gmail import fetch_emails
    print("   ✓ Gmail imported")
    
    print("5. Creating FastAPI app...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="Debug Test", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    def root():
        return {"message": "Debug test working!"}
    
    print("   ✓ FastAPI app created")
    
    print("6. Testing uvicorn import...")
    import uvicorn
    print("   ✓ Uvicorn imported")
    
    print("7. Starting server...")
    print("   Starting uvicorn.run()...")
    uvicorn.run(app, host="127.0.0.1", port=8031, log_level="info")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc() 