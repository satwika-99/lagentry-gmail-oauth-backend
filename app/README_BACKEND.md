# Lagentry OAuth Backend

A comprehensive OAuth 2.0 backend service for Lagentry AI agents, supporting multiple OAuth providers including Google, Microsoft, Atlassian, Slack, and Notion.

## 🚀 Features

- **Multi-Provider OAuth**: Google, Microsoft, Atlassian, Slack, Notion
- **Unified Authentication**: Single interface for all OAuth providers
- **Token Management**: Secure storage and refresh of OAuth tokens
- **RESTful API**: FastAPI-based REST API with automatic documentation
- **Database Integration**: SQLite database for token storage
- **CORS Support**: Configurable CORS for frontend integration
- **Health Monitoring**: Built-in health check endpoints

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ilura-ai/lagentry-app.git
   cd lagentry-app/app_new
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the `app` directory with your OAuth credentials:
   
   ```env
   # Google OAuth
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_REDIRECT_URI=http://127.0.0.1:8081/auth/google/callback
   
   # Atlassian/Jira OAuth
   ATLASSIAN_CLIENT_ID=your_atlassian_client_id
   ATLASSIAN_CLIENT_SECRET=your_atlassian_client_secret
   ATLASSIAN_REDIRECT_URI=http://127.0.0.1:8081/api/v1/auth/atlassian/callback
   
   # Server Configuration
   PORT=8081
   HOST=127.0.0.1
   DEBUG=true
   DATABASE_PATH=oauth_tokens.db
   
   # Security
   SECRET_KEY=your-secret-key-here
   TOKEN_EXPIRY_HOURS=24
   ```

## 🚀 Running the Backend

### Option 1: Using the startup script (Recommended)
```bash
python start_backend.py
```

### Option 2: Direct uvicorn command
```bash
uvicorn main:app --host 127.0.0.1 --port 8081 --reload
```

### Option 3: Python module execution
```bash
python -m main
```

## 🌐 API Endpoints

### Base URL
```
http://127.0.0.1:8081
```

### Core Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### Authentication Endpoints
- `GET /api/v1/auth/google/authorize` - Google OAuth authorization
- `GET /api/v1/auth/google/callback` - Google OAuth callback
- `GET /api/v1/auth/atlassian/authorize` - Atlassian OAuth authorization
- `GET /api/v1/auth/atlassian/callback` - Atlassian OAuth callback
- `GET /api/v1/auth/slack/authorize` - Slack OAuth authorization
- `GET /api/v1/auth/slack/callback` - Slack OAuth callback

### Provider-Specific Endpoints
- `GET /api/v1/google/emails` - Fetch Gmail emails
- `GET /api/v1/atlassian/jira` - Jira integration
- `GET /api/v1/slack/channels` - Slack channels
- `GET /api/v1/microsoft/emails` - Outlook emails

### Unified Endpoints
- `GET /api/v1/unified/auth` - Unified authentication status
- `GET /api/v1/unified/providers` - List available providers

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `127.0.0.1` |
| `PORT` | Server port | `8081` |
| `DEBUG` | Debug mode | `false` |
| `DATABASE_PATH` | SQLite database path | `oauth_tokens.db` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Required |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | Required |
| `ATLASSIAN_CLIENT_ID` | Atlassian OAuth client ID | Required |
| `ATLASSIAN_CLIENT_SECRET` | Atlassian OAuth client secret | Required |

### CORS Configuration
CORS origins are configurable via the `CORS_ORIGINS` environment variable. Default origins include:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8000`
- `http://127.0.0.1:8000`
- `http://127.0.0.1:8081`

## 🗄️ Database

The backend uses SQLite for token storage. The database file (`oauth_tokens.db`) is automatically created on first run.

### Database Schema
- **users**: User information and authentication details
- **oauth_tokens**: OAuth tokens for different providers
- **provider_connections**: Active provider connections

## 🔒 Security Features

- OAuth 2.0 standard compliance
- Secure token storage
- Configurable token expiry
- CORS protection
- Input validation with Pydantic
- Global exception handling

## 🧪 Testing

### Health Check
```bash
curl http://127.0.0.1:8081/health
```

### API Documentation
Open your browser and navigate to:
```
http://127.0.0.1:8081/docs
```

## 📁 Project Structure

```
app/
├── api/                    # API endpoints
│   └── v1/               # API version 1
├── core/                  # Core functionality
│   ├── config.py         # Configuration management
│   ├── database.py       # Database operations
│   ├── auth.py           # Authentication utilities
│   └── exceptions.py     # Custom exceptions
├── providers/             # OAuth provider implementations
│   ├── google/           # Google OAuth
│   ├── atlassian/        # Atlassian OAuth
│   ├── slack/            # Slack OAuth
│   └── microsoft/        # Microsoft OAuth
├── services/              # Business logic services
├── models/                # Data models
├── schemas/               # Pydantic schemas
├── storage/               # Storage utilities
├── main.py               # FastAPI application
├── start_backend.py      # Startup script
├── requirements.txt      # Python dependencies
└── README_BACKEND.md     # This file
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `.env` file or use a different port
   - Kill processes using the port: `lsof -ti:8081 | xargs kill -9`

2. **OAuth configuration errors**
   - Verify all required environment variables are set
   - Check OAuth redirect URIs match exactly
   - Ensure OAuth apps are properly configured in provider dashboards

3. **Database errors**
   - Check file permissions for database directory
   - Verify `DATABASE_PATH` environment variable

4. **Import errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

### Debug Mode
Enable debug mode by setting `DEBUG=true` in your `.env` file for detailed error messages and automatic reloading.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Lagentry AI platform. See the main repository for license information.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the troubleshooting section
- Open an issue on GitHub
- Contact the Lagentry team

---

**Happy coding! 🎉**
