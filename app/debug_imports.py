#!/usr/bin/env python3

print("Testing imports...")

try:
    print("1. Testing config import...")
    from config import config
    print("   ✓ Config imported successfully")
    print(f"   - Database path: {config.DATABASE_PATH}")
    print(f"   - Server port: {config.SERVER_PORT}")
except Exception as e:
    print(f"   ✗ Config import failed: {e}")

try:
    print("2. Testing storage import...")
    from storage import init_db, get_db_connection
    print("   ✓ Storage imported successfully")
except Exception as e:
    print(f"   ✗ Storage import failed: {e}")

try:
    print("3. Testing auth import...")
    from auth import generate_auth_url, handle_oauth_callback
    print("   ✓ Auth imported successfully")
except Exception as e:
    print(f"   ✗ Auth import failed: {e}")

try:
    print("4. Testing gmail import...")
    from gmail import fetch_emails, fetch_email_content
    print("   ✓ Gmail imported successfully")
except Exception as e:
    print(f"   ✗ Gmail import failed: {e}")

try:
    print("5. Testing main app import...")
    from main import app
    print("   ✓ Main app imported successfully")
    print(f"   - App title: {app.title}")
    print(f"   - App version: {app.version}")
except Exception as e:
    print(f"   ✗ Main app import failed: {e}")

print("\nAll import tests completed!") 