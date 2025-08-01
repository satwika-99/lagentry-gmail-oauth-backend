#!/usr/bin/env python3

print("=== Testing Main App Imports ===")

try:
    print("1. Testing config...")
    from config import config
    print("   ✓ Config imported")
    
    print("2. Testing storage...")
    from storage import init_db
    print("   ✓ Storage imported")
    
    print("3. Testing auth...")
    from auth import generate_auth_url
    print("   ✓ Auth imported")
    
    print("4. Testing gmail...")
    from gmail import fetch_emails
    print("   ✓ Gmail imported")
    
    print("5. Testing FastAPI...")
    from fastapi import FastAPI
    from fastapi.middleware.wsgi import WSGIMiddleware
    print("   ✓ FastAPI imported")
    
    print("6. Creating app...")
    app = FastAPI()
    print("   ✓ App created")
    
    print("7. Converting to WSGI...")
    wsgi_app = WSGIMiddleware(app)
    print("   ✓ WSGI conversion successful")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 