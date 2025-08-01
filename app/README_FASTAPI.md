# Gmail OAuth Backend for Lagentry AI Agents

A custom FastAPI-based Gmail OAuth 2.0 backend that enables Lagentry AI agents to access Gmail after user authorization. This module replicates the working OAuth setup from n8n as a standalone microservice.

## Features

- ✅ **OAuth 2.0 Flow**: Complete Google OAuth implementation
- ✅ **Token Management**: Secure storage and automatic refresh of access/refresh tokens
- ✅ **Gmail API Integration**: Fetch emails with full metadata
- ✅ **Modular Design**: Clean architecture for easy extension to other providers
- ✅ **FastAPI**: Modern, fast, and auto-documented API
- ✅ **SQLite Storage**: Lightweight token persistence
- ✅ **CORS Support**: Ready for frontend integration

## Quick Start

### 1. Environment Setup

Create a `.env` file in the `app` directory:

```bash
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
REDIRECT_URI=http://127.0.0.1:8050/auth/google/callback
DATABASE_PATH=oauth_tokens.db
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn httpx python-dotenv pydantic
```

### 3. Run the Server

```bash
python fastapi_gmail_oauth.py
```

The server will start on `http://127.0.0.1:8050`

### 4. Access API Documentation

Visit `http://127.0.0.1:8050/docs` for interactive API documentation.

## API Endpoints

### Authentication Flow

#### 1. Initiate OAuth
```
GET /auth/google
```
Redirects user to Google's OAuth consent screen.

#### 2. OAuth Callback
```
GET /auth/google/callback?code={code}&state={state}
```
Handles the OAuth callback and stores tokens.

**Response:**
```json
{
  "message": "OAuth successful",
  "user_email": "user@example.com",
  "access_token": "ya29.a0AfH6SMC...",
  "expires_in": 3600
}
```

### Email Operations

#### 3. Fetch Emails
```
GET /emails?user_email={email}&max_results={count}
```
Fetches latest emails for authenticated user.

**Response:**
```json
{
  "emails": [
    {
      "id": "message_id",
      "thread_id": "thread_id",
      "subject": "Email Subject",
      "sender": "sender@example.com",
      "date": "Wed, 1 Aug 2024 10:00:00 +0000",
      "snippet": "Email preview text..."
    }
  ]
}
```

### Management Endpoints

#### 4. List Users
```
GET /users
```
Returns all users with stored tokens.

#### 5. Health Check
```
GET /health
```
Returns server health status.

#### 6. Root Endpoint
```
GET /
```
Returns API information and available endpoints.

## OAuth Flow for Lagentry Integration

### Step 1: User Initiates Connection
When a user clicks "Connect Gmail" in the Lagentry UI:

```javascript
// Frontend redirects to OAuth endpoint
window.location.href = 'http://127.0.0.1:8050/auth/google';
```

### Step 2: Google OAuth Consent
User is redirected to Google's consent screen where they authorize the application.

### Step 3: Token Storage
After authorization, tokens are automatically stored in the SQLite database.

### Step 4: AI Agent Access
Lagentry AI agents can now access Gmail using the stored tokens:

```python
# Example: Fetch emails for a user
response = requests.get(
    'http://127.0.0.1:8050/emails',
    params={'user_email': 'user@example.com', 'max_results': 10}
)
emails = response.json()['emails']
```

## Database Schema

The application uses SQLite to store OAuth tokens:

```sql
CREATE TABLE oauth_tokens (
    user_email TEXT PRIMARY KEY,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

- **Token Refresh**: Automatic refresh of expired access tokens
- **Partial Token Display**: Only shows first 20 characters of access tokens in responses
- **State Parameter**: OAuth state parameter for CSRF protection
- **CORS Configuration**: Proper CORS setup for frontend integration
- **Error Handling**: Comprehensive error handling and logging

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | Required |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | Required |
| `REDIRECT_URI` | OAuth callback URL | `http://127.0.0.1:8050/auth/google/callback` |
| `DATABASE_PATH` | SQLite database path | `oauth_tokens.db` |

## Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (marine-balm-467515-s8)
3. Navigate to "APIs & Services" > "Credentials"
4. Create or use existing OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://127.0.0.1:8050/auth/google/callback`
   - `http://localhost:8050/auth/google/callback`

## Extending for Other Providers

The modular design makes it easy to extend for other providers:

1. **Create new OAuth module** (e.g., `outlook_auth.py`)
2. **Add provider-specific endpoints** (e.g., `/auth/outlook`)
3. **Implement provider API functions** (e.g., `fetch_outlook_emails`)
4. **Update database schema** if needed

## Testing

### Test OAuth Flow
1. Start the server: `python fastapi_gmail_oauth.py`
2. Visit: `http://127.0.0.1:8050/auth/google`
3. Complete OAuth flow
4. Check tokens are stored: `GET /users`

### Test Email Fetching
1. After OAuth, fetch emails: `GET /emails?user_email=your@email.com`
2. Verify email data is returned correctly

## Troubleshooting

### Common Issues

1. **"Google Client ID not configured"**
   - Check your `.env` file has correct `GOOGLE_CLIENT_ID`

2. **"OAuth callback failed"**
   - Verify redirect URI matches Google Cloud Console settings
   - Check network connectivity

3. **"No valid tokens found for user"**
   - User needs to complete OAuth flow first
   - Check database for stored tokens

4. **Port already in use**
   - Change port in the script or kill existing process
   - Update redirect URI accordingly

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export PYTHONPATH=.
python -m uvicorn fastapi_gmail_oauth:app --reload --host 127.0.0.1 --port 8050
```

## Production Deployment

For production deployment:

1. **Use HTTPS**: Update redirect URIs to use HTTPS
2. **Database**: Consider PostgreSQL for production
3. **Environment**: Use proper environment variable management
4. **Monitoring**: Add logging and monitoring
5. **Security**: Implement rate limiting and additional security measures

## License

This project is part of the Lagentry AI platform. 