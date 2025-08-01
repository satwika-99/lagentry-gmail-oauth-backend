# Gmail OAuth Backend

A FastAPI-based backend service that implements Gmail OAuth 2.0 flow for Lagentry AI agents to access Gmail after user authorization.

## Features

-  Complete OAuth 2.0 flow with Google
-  Secure token storage in SQLite database
-  Automatic token refresh
-  Gmail API integration
-  CORS support for frontend integration
-  Modular design for future provider extensions

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
# Google OAuth Credentials (from Google Cloud Console)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# OAuth Redirect URI
REDIRECT_URI=http://localhost:8000/auth/google/callback

# Optional: Custom port
PORT=8000
```

### 3. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (marine-balm-467515-s8)
3. Navigate to "APIs & Services" > "Credentials"
4. Create or use existing OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback` (for development)
   - Your production callback URL

### 4. Enable Gmail API

1. In Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click "Enable"

### 5. Run the Server

```bash
python start.py
```

Or with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Authentication Flow

1. **GET /auth/google**
   - Initiates OAuth flow
   - Redirects user to Google consent screen

2. **GET /auth/google/callback**
   - Handles OAuth callback
   - Exchanges authorization code for tokens
   - Stores tokens securely

### Email Operations

3. **GET /emails?user_email=user@example.com&max_results=10**
   - Fetches emails from Gmail
   - Requires valid OAuth tokens
   - Returns email list with details

### Utility Endpoints

4. **GET /**
   - API information and available endpoints

5. **GET /status**
   - Service status and configuration info

## Usage Examples

### 1. Complete OAuth Flow

```bash
# 1. Start the server
python start.py

# 2. Open browser to initiate OAuth
curl http://localhost:8000/auth/google
# This will redirect to Google consent screen

# 3. After authorization, tokens are stored automatically
```

### 2. Fetch Emails

```bash
# Get emails for authenticated user
curl "http://localhost:8000/emails?user_email=user@example.com&max_results=5"
```

### 3. Check Status

```bash
# Check API status and configuration
curl http://localhost:8000/status
```

## Testing

Run the test suite:

```bash
python test_setup.py
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | Yes | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | Yes | - |
| `REDIRECT_URI` | OAuth callback URL | No | `http://localhost:8000/auth/google/callback` |
| `PORT` | Server port | No | `8000` |

## OAuth Scopes

The application requests the following Gmail scopes:

- `https://www.googleapis.com/auth/gmail.readonly` - Read Gmail messages
- `https://www.googleapis.com/auth/userinfo.email` - Get user email address

## Frontend Integration

For Lagentry UI integration, the frontend should:

1. Redirect users to `/auth/google` to start OAuth flow
2. Handle the callback at `/auth/google/callback`
3. Use the stored tokens to call `/emails` endpoint

Example frontend flow:

```javascript
// 1. Redirect to OAuth
window.location.href = 'http://localhost:8000/auth/google';

// 2. After OAuth, call emails endpoint
const response = await fetch('http://localhost:8000/emails?user_email=user@example.com');
const emails = await response.json();
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad request (missing parameters)
- `401` - Unauthorized (invalid/missing tokens)
- `500` - Server error

## Troubleshooting

### Common Issues

1. **"Google Client ID not configured"**
   - Check your `.env` file
   - Ensure `GOOGLE_CLIENT_ID` is set

2. **"OAuth error"**
   - Verify redirect URI matches Google Cloud Console
   - Check client secret is correct
   - Ensure Gmail API is enabled

3. **"No valid tokens found"**
   - Complete OAuth flow first
   - Check database for stored tokens

4. **"Token refresh failed"**
   - User may need to re-authenticate
   - Check refresh token validity

## License

This project is part of the Lagentry AI agent system.
