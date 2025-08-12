import os
from dotenv import load_dotenv
from app.providers.google.auth import GoogleOAuthProvider

# Load environment variables
load_dotenv('env_test.txt')

# Create Google OAuth provider
google_provider = GoogleOAuthProvider()

print("=== OAuth Configuration Test ===")
print(f"Client ID: {google_provider.client_id}")
print(f"Redirect URI: {google_provider.redirect_uri}")
print(f"Scopes: {google_provider.scopes}")

# Generate OAuth URL
auth_url = google_provider.get_auth_url()
print(f"\n=== Generated OAuth URL ===")
print(auth_url)

# Check if redirect URI matches Google Console
expected_redirect = "http://127.0.0.1:54321/api/v1/google/auth/callback"
if google_provider.redirect_uri == expected_redirect:
    print(f"\n✅ Redirect URI matches: {google_provider.redirect_uri}")
else:
    print(f"\n❌ Redirect URI mismatch!")
    print(f"Expected: {expected_redirect}")
    print(f"Actual: {google_provider.redirect_uri}")
