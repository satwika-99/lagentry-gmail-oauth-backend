#!/usr/bin/env python3
import sqlite3
from config import config

def debug_tokens():
    print("=== DEBUGGING TOKEN DATA TYPES ===")
    
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM oauth_tokens;")
        tokens = cursor.fetchall()
        
        for token in tokens:
            print(f"User: {token[1]}")
            print(f"Access Token Type: {type(token[2])} - Value: {token[2][:20] if token[2] else 'None'}...")
            print(f"Refresh Token Type: {type(token[3])} - Value: {token[3][:20] if token[3] else 'None'}...")
            print(f"Expires At Type: {type(token[4])} - Value: {token[4]}")
            print(f"Created At Type: {type(token[5])} - Value: {token[5]}")
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_tokens() 