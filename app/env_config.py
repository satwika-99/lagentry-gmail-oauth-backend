# Google OAuth Configuration
# Replace these with your actual Google Cloud OAuth credentials
GOOGLE_CLIENT_ID = "your_client_id_here"
GOOGLE_CLIENT_SECRET = "your_client_secret_here"

# Server Configuration
PORT = 8010
HOST = "127.0.0.1"

# Redirect URI (must match what you configure in Google Cloud Console)
REDIRECT_URI = "http://127.0.0.1:8010/auth/google/callback"

# Database Configuration
DATABASE_PATH = "oauth_tokens.db"

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000", 
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

# Instructions for setting up Google OAuth:
"""
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Select your project: marine-balm-467515-s8
3. Go to APIs & Services > Credentials
4. Create or edit OAuth 2.0 Client ID
5. Add these Authorized redirect URIs:
   - http://127.0.0.1:8010/auth/google/callback
   - http://localhost:8010/auth/google/callback
6. Copy the Client ID and Client Secret
7. Update the values above
""" 