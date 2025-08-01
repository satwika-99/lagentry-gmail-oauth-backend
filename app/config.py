import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Gmail OAuth Backend"""
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/google/callback")
    
    # Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "oauth_tokens.db")
    
    # Gmail API Configuration
    SCOPES: list = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/userinfo.email"
    ]
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.GOOGLE_CLIENT_ID:
            print(" GOOGLE_CLIENT_ID not set")
            return False
        
        if not cls.GOOGLE_CLIENT_SECRET:
            print(" GOOGLE_CLIENT_SECRET not set")
            return False
        
        print(" Configuration validated")
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without secrets)"""
        print(" Current Configuration:")
        print(f"  Google Client ID: {' Set' if cls.GOOGLE_CLIENT_ID else ' Not Set'}")
        print(f"  Google Client Secret: {' Set' if cls.GOOGLE_CLIENT_SECRET else ' Not Set'}")
        print(f"  Redirect URI: {cls.REDIRECT_URI}")
        print(f"  Server Port: {cls.PORT}")
        print(f"  Database Path: {cls.DATABASE_PATH}")
        print(f"  CORS Origins: {cls.CORS_ORIGINS}")

# Create global config instance
config = Config()
