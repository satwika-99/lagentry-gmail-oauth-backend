# Lagentry Gmail OAuth Backend

A custom FastAPI-based Gmail OAuth 2.0 backend that enables Lagentry AI agents to access Gmail after user authorization.

## Quick Start

### 1. Environment Setup

Create a `.env` file in the `app` directory:

```bash
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
REDIRECT_URI=http://127.0.0.1:8080/auth/google/callback
DATABASE_PATH=oauth_tokens.db
```

### 2. Install Dependencies

**Windows (PowerShell):**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r app/requirements.txt
```

**Linux/Mac:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt
```

### 3. Run the Server

**Option 1: Using the startup script (Recommended)**
```powershell
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
python start_server.py
```

```bash
# Linux/Mac
source venv/bin/activate
python start_server.py
```

**Option 2: Direct execution**
```powershell
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
python app/main.py
```

```bash
# Linux/Mac
source venv/bin/activate
python app/main.py
```

The server will start on `http://127.0.0.1:8080`

### 4. Access API Documentation

Visit `http://127.0.0.1:8080/docs` for interactive API documentation.

## API Endpoints

- `GET /` - API information
- `GET /auth/google` - Initiate OAuth flow
- `GET /auth/google/callback` - OAuth callback handler
- `GET /emails` - Fetch emails for authenticated user
- `GET /users` - List all users with stored tokens
- `GET /health` - Health check

## Features

- ✅ **OAuth 2.0 Flow**: Complete Google OAuth implementation
- ✅ **Token Management**: Secure storage and automatic refresh of access/refresh tokens
- ✅ **Gmail API Integration**: Fetch emails with full metadata
- ✅ **FastAPI**: Modern, fast, and auto-documented API
- ✅ **SQLite Storage**: Lightweight token persistence
- ✅ **CORS Support**: Ready for frontend integration

## Documentation

For detailed documentation, see [app/README_FASTAPI.md](app/README_FASTAPI.md)
