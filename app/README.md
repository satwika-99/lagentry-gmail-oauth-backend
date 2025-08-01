# Gmail OAuth Backend for Lagentry

A modular FastAPI-based backend service that implements Gmail OAuth 2.0 flow for Lagentry AI agents to access Gmail after user authorization.

## 🚀 Features

- ✅ **Complete OAuth 2.0 Flow** - Secure Google OAuth implementation
- ✅ **Modular Architecture** - Clean separation of concerns (auth, gmail, storage)
- ✅ **Token Management** - Automatic refresh and secure storage
- ✅ **Gmail API Integration** - Fetch, search, and read emails
- ✅ **CORS Support** - Frontend integration ready
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **Extensible Design** - Easy to add other providers (Outlook, Slack, etc.)

## 📁 Project Structure

```
app/
├── main.py          # FastAPI application and routes
├── auth.py          # OAuth authentication logic
├── gmail.py         # Gmail API integration
├── storage.py       # Token storage and database operations
├── config.py        # Configuration management
├── requirements.txt  # Python dependencies
├── start.py         # Server startup script
└── README.md        # This file
```

## 🛠️ Quick Start

### 1. Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the `app` directory:

```env
# Google OAuth Credentials (from Google Cloud Console)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# OAuth Redirect URI (must match Google Cloud Console)
REDIRECT_URI=http://localhost:8000/auth/google/callback

# Optional: Custom port
PORT=8000
HOST=0.0.0.0
```

### 3. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (marine-balm-467515-s8)
3. Navigate to "APIs & Services" > "Credentials"
4. Create or use existing OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback` (development)
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

## 🔌 API Endpoints

### Authentication Flow

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/google` | Start OAuth flow |
| `GET` | `/auth/google/callback` | Handle OAuth callback |

### Email Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/emails` | Fetch inbox emails |
| `GET` | `/emails/{message_id}` | Get specific email content |
| `GET` | `/emails/search` | Search emails |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/users` | List authenticated users |
| `GET` | `/status` | Service status |

## 📖 Usage Examples

### 1. Complete OAuth Flow

```bash
# Start the server
python start.py

# Visit in browser to start OAuth
http://localhost:8000/auth/google
```

### 2. Fetch Emails

```bash
# Get latest emails
curl "http://localhost:8000/emails?user_email=user@example.com&max_results=5"

# Search emails
curl "http://localhost:8000/emails/search?user_email=user@example.com&query=from:important@company.com"

# Get specific email content
curl "http://localhost:8000/emails/18b7c0f8a1b2c3d4?user_email=user@example.com"
```

### 3. Check Status

```bash
# Check API status
curl http://localhost:8000/status

# List authenticated users
curl http://localhost:8000/users
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | Yes | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | Yes | - |
| `REDIRECT_URI` | OAuth callback URL | No | `http://localhost:8000/auth/google/callback` |
| `PORT` | Server port | No | `8000` |
| `HOST` | Server host | No | `0.0.0.0` |

### OAuth Scopes

The application requests these Gmail scopes:

- `https://www.googleapis.com/auth/gmail.readonly` - Read Gmail messages
- `https://www.googleapis.com/auth/userinfo.email` - Get user email address

## 🏗️ Architecture

### Modular Design

The application is organized into focused modules:

- **`auth.py`** - OAuth 2.0 flow, token refresh, user authentication
- **`gmail.py`** - Gmail API calls, email operations, search functionality
- **`storage.py`** - Database operations, token storage, user management
- **`config.py`** - Configuration management and validation
- **`main.py`** - FastAPI routes and application setup

### Database Schema

```sql
CREATE TABLE oauth_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT UNIQUE,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔒 Security Features

- **State Parameter** - CSRF protection in OAuth flow
- **Token Encryption** - Secure storage of access/refresh tokens
- **Automatic Refresh** - Tokens refreshed before expiration
- **CORS Protection** - Configurable CORS origins
- **Error Handling** - No sensitive data in error responses

## 🧪 Testing

Run the test suite:

```bash
python test_setup.py
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔄 Frontend Integration

For Lagentry UI integration:

```javascript
// 1. Redirect to OAuth
window.location.href = 'http://localhost:8000/auth/google';

// 2. After OAuth, fetch emails
const response = await fetch('http://localhost:8000/emails?user_email=user@example.com');
const emails = await response.json();

// 3. Search emails
const searchResponse = await fetch('http://localhost:8000/emails/search?user_email=user@example.com&query=important');
const searchResults = await searchResponse.json();
```

## 🚀 Deployment

### Development

```bash
python start.py
```

### Production

```bash
# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Using gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Troubleshooting

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

## 🔮 Future Extensions

The modular design makes it easy to add other providers:

- **Outlook/Microsoft Graph** - Add `outlook.py` module
- **Slack** - Add `slack.py` module
- **Discord** - Add `discord.py` module
- **Database Support** - PostgreSQL, MongoDB, Redis
- **Caching** - Redis for token caching
- **Monitoring** - Prometheus metrics, health checks

## 📄 License

This project is part of the Lagentry AI agent system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Ready to power your Lagentry AI agents with Gmail access! 🚀** 