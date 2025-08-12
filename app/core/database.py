"""
Database management for the Lagentry OAuth Backend
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from .config import settings


class DatabaseManager:
    """Manages database operations for OAuth tokens and user data"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database_path
    
    def init_db(self) -> None:
        """Initialize the database with required tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # OAuth tokens table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS oauth_tokens (
                        user_email TEXT PRIMARY KEY,
                        provider TEXT NOT NULL,
                        access_token TEXT NOT NULL,
                        refresh_token TEXT NOT NULL,
                        expires_at TIMESTAMP NOT NULL,
                        scopes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        name TEXT,
                        provider TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Connectors table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS connectors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        provider TEXT NOT NULL,
                        connector_type TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        config TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_email) REFERENCES users (email)
                    )
                ''')
                
                # Activity log table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS activity_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        provider TEXT NOT NULL,
                        action TEXT NOT NULL,
                        details TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_email) REFERENCES users (email)
                    )
                ''')
                
                conn.commit()
                print(f"Database initialized at: {self.db_path}")
                
        except Exception as e:
            print(f"Database initialization failed: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def store_tokens(self, user_email: str, provider: str, access_token: str, 
                    refresh_token: str, expires_in: int, scopes: Optional[List[str]] = None) -> bool:
        """Store OAuth tokens for a user"""
        try:
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            scopes_json = json.dumps(scopes) if scopes else None
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO oauth_tokens 
                    (user_email, provider, access_token, refresh_token, expires_at, scopes, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_email, provider, access_token, refresh_token, expires_at, scopes_json, datetime.now()))
                
                # Also update users table
                cursor.execute('''
                    INSERT OR REPLACE INTO users (email, provider, updated_at)
                    VALUES (?, ?, ?)
                ''', (user_email, provider, datetime.now()))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Failed to store tokens: {e}")
            return False
    
    def get_valid_tokens(self, user_email: str, provider: str) -> Optional[Dict[str, Any]]:
        """Get valid tokens for a user and provider"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM oauth_tokens 
                    WHERE user_email = ? AND provider = ? AND expires_at > ?
                ''', (user_email, provider, datetime.now()))
                
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            print(f"Failed to get tokens: {e}")
            return None
    
    def refresh_tokens(self, user_email: str, provider: str, new_access_token: str, 
                      new_refresh_token: str, expires_in: int) -> bool:
        """Update tokens after refresh"""
        try:
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE oauth_tokens 
                    SET access_token = ?, refresh_token = ?, expires_at = ?, updated_at = ?
                    WHERE user_email = ? AND provider = ?
                ''', (new_access_token, new_refresh_token, expires_at, datetime.now(), user_email, provider))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Failed to refresh tokens: {e}")
            return False
    
    def get_all_users(self, provider: Optional[str] = None) -> List[str]:
        """Get all users with stored tokens"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if provider:
                    cursor.execute('''
                        SELECT DISTINCT user_email FROM oauth_tokens 
                        WHERE provider = ? AND expires_at > ?
                    ''', (provider, datetime.now()))
                else:
                    cursor.execute('''
                        SELECT DISTINCT user_email FROM oauth_tokens 
                        WHERE expires_at > ?
                    ''', (datetime.now(),))
                
                return [row['user_email'] for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Failed to get users: {e}")
            return []
    
    def delete_user_tokens(self, user_email: str, provider: str) -> bool:
        """Delete tokens for a user and provider"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM oauth_tokens 
                    WHERE user_email = ? AND provider = ?
                ''', (user_email, provider))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Failed to delete tokens: {e}")
            return False
    
    def log_activity(self, user_email: str, provider: str, action: str, details: Optional[Dict] = None) -> bool:
        """Log user activity"""
        try:
            details_json = json.dumps(details) if details else None
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO activity_log (user_email, provider, action, details)
                    VALUES (?, ?, ?, ?)
                ''', (user_email, provider, action, details_json))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Failed to log activity: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager() 