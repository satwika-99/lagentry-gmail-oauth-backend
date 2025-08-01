"""
Token storage module for Gmail OAuth Backend
Handles secure storage and retrieval of OAuth tokens
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import config

def init_db():
    """Initialize SQLite database for token storage"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oauth_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE,
            access_token TEXT,
            refresh_token TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(config.DATABASE_PATH)

def store_tokens(user_email: str, access_token: str, refresh_token: str, expires_in: int):
    """Store OAuth tokens in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    expires_at = datetime.now() + timedelta(seconds=expires_in)
    
    cursor.execute("""
        INSERT OR REPLACE INTO oauth_tokens 
        (user_email, access_token, refresh_token, expires_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_email, access_token, refresh_token, expires_at, datetime.now()))
    
    conn.commit()
    conn.close()

def get_valid_tokens(user_email: str) -> Optional[Dict[str, Any]]:
    """Get valid tokens for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT access_token, refresh_token, expires_at 
        FROM oauth_tokens 
        WHERE user_email = ?
    """, (user_email,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        access_token, refresh_token, expires_at = result
        expires_at = datetime.fromisoformat(expires_at)
        
        # Check if token is still valid
        if datetime.now() < expires_at:
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at
            }
    
    return None

def delete_tokens(user_email: str):
    """Delete tokens for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM oauth_tokens WHERE user_email = ?", (user_email,))
    conn.commit()
    conn.close()

def get_all_users():
    """Get list of all users with stored tokens"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_email, expires_at FROM oauth_tokens")
    results = cursor.fetchall()
    conn.close()
    
    return [{"email": row[0], "expires_at": row[1]} for row in results]
