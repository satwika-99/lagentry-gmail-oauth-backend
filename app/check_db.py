#!/usr/bin/env python3
import sqlite3
import os
from config import config

def check_database():
    print("=== DATABASE CHECK ===")
    
    # Check if database file exists
    if os.path.exists(config.DATABASE_PATH):
        print(f"✅ Database file exists: {config.DATABASE_PATH}")
    else:
        print(f"❌ Database file not found: {config.DATABASE_PATH}")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables in database: {[table[0] for table in tables]}")
        
        # Check oauth_tokens table
        if ('oauth_tokens',) in tables:
            cursor.execute("SELECT * FROM oauth_tokens;")
            tokens = cursor.fetchall()
            print(f"🔑 Found {len(tokens)} token records:")
            
            for token in tokens:
                print(f"  - User: {token[1]}")
                print(f"    Access Token: {token[2][:20]}..." if token[2] else "    Access Token: None")
                print(f"    Refresh Token: {token[3][:20]}..." if token[3] else "    Refresh Token: None")
                print(f"    Expires At: {token[4]}")
                print(f"    Created At: {token[5]}")
                print()
        else:
            print("❌ oauth_tokens table not found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

if __name__ == "__main__":
    check_database() 