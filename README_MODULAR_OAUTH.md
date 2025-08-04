# Lagentry Modular OAuth Backend

A scalable, modular OAuth 2.0 backend for Lagentry AI agents supporting multiple providers (Google, Slack, Atlassian) with a unified API interface.

## 🏗️ Architecture Overview

The refactored codebase follows a modular, scalable architecture with clear separation of concerns:

```
app/
├── connectors/           # Connector implementations
│   ├── base.py         # Base connector classes
│   ├── google/         # Google connectors
│   ├── slack/          # Slack connectors
│   └── atlassian/      # Atlassian connectors
├── providers/           # OAuth provider implementations
│   ├── google/         # Google OAuth
│   ├── slack/          # Slack OAuth
│   └── atlassian/      # Atlassian OAuth
├── services/            # Business logic services
│   ├── oauth_service.py    # Unified OAuth service
│   └── connector_service.py # Unified connector service
├── api/v1/             # API endpoints
│   ├── unified.py      # Unified API router
│   └── ...             # Provider-specific routers
└── core/               # Core functionality
    ├── config.py       # Configuration management
    ├── database.py     # Database operations
    └── auth.py         # Base OAuth classes
```

## 🎯 Key Features

### ✅ Modular Design
- **Provider Isolation**: Each OAuth provider is self-contained
- **Connector Pattern**: Unified interface for all data operations
- **Factory Pattern**: Easy addition of new providers
- **Service Layer**: Clean separation of business logic

### ✅ Supported Providers
- **Google**: Gmail, Drive, Calendar
- **Slack**: Channels, Messages, Users
- **Atlassian**: Jira, Confluence, Bitbucket

### ✅ Unified API
- Single endpoint structure for all providers
- Consistent response formats
- Comprehensive error handling
- Activity logging and monitoring

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r app/requirements.txt

# Set up environment variables
cp app/env_example.txt .env
# Edit .env with your OAuth credentials
```

### 2. Configuration

Add your OAuth credentials to `.env`:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Slack OAuth
SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret

# Atlassian OAuth
ATLASSIAN_CLIENT_ID=your_atlassian_client_id
ATLASSIAN_CLIENT_SECRET=your_atlassian_client_secret
```

### 3. Run the Server

```bash
# Start the server
python -m app.main

# Or use the start script
python start_server.py
```

The server will be available at `http://127.0.0.1:8081`

## 📚 API Documentation

### Unified API Endpoints

#### OAuth Authentication
```
GET  /api/v1/unified/auth/{provider}/url      # Get OAuth URL
GET  /api/v1/unified/auth/{provider}/callback # Handle OAuth callback
GET  /api/v1/unified/auth/{provider}/validate # Validate tokens
GET  /api/v1/unified/auth/{provider}/refresh  # Refresh tokens
DELETE /api/v1/unified/auth/{provider}/revoke # Revoke tokens
GET  /api/v1/unified/auth/status              # Get user status
GET  /api/v1/unified/auth/providers           # List available providers
```

#### Connector Operations
```
GET  /api/v1/unified/connectors               # List available connectors
GET  /api/v1/unified/connectors/{provider}/test      # Test connection
GET  /api/v1/unified/connectors/{provider}/capabilities # Get capabilities
GET  /api/v1/unified/connectors/{provider}/items     # List items
GET  /api/v1/unified/connectors/{provider}/items/{id} # Get item
POST /api/v1/unified/connectors/{provider}/items     # Create item
PUT  /api/v1/unified/connectors/{provider}/items/{id} # Update item
DELETE /api/v1/unified/connectors/{provider}/items/{id} # Delete item
GET  /api/v1/unified/connectors/{provider}/search    # Search items
```

#### Provider-Specific Endpoints

**Slack:**
```
GET  /api/v1/unified/slack/channels                    # List channels
POST /api/v1/unified/slack/channels/{id}/messages     # Send message
```

**Jira:**
```
GET  /api/v1/unified/jira/projects                    # List projects
GET  /api/v1/unified/jira/projects/{id}/issues        # List issues
GET  /api/v1/unified/jira/my-issues                   # Get my issues
```

**Gmail:**
```
GET  /api/v1/unified/gmail/emails                     # List emails
POST /api/v1/unified/gmail/send                       # Send email
GET  /api/v1/unified/gmail/labels                     # Get labels
```

## 🔧 Connector Architecture

### Base Connector Classes

```python
# Data Connector (for emails, files, etc.)
class DataConnector(BaseConnector):
    async def list_items(self, **kwargs) -> Dict[str, Any]
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]
    async def delete_item(self, item_id: str, **kwargs) -> bool
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]

# Communication Connector (for messages, channels, etc.)
class CommunicationConnector(BaseConnector):
    async def list_channels(self, **kwargs) -> Dict[str, Any]
    async def get_channel(self, channel_id: str, **kwargs) -> Dict[str, Any]
    async def list_messages(self, channel_id: str, **kwargs) -> Dict[str, Any]
    async def send_message(self, channel_id: str, message: str, **kwargs) -> Dict[str, Any]

# Project Connector (for issues, tasks, etc.)
class ProjectConnector(BaseConnector):
    async def list_projects(self, **kwargs) -> Dict[str, Any]
    async def get_project(self, project_id: str, **kwargs) -> Dict[str, Any]
    async def list_issues(self, project_id: str, **kwargs) -> Dict[str, Any]
    async def create_issue(self, project_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]
```

### Connector Factory

```python
from app.connectors import ConnectorFactory

# Register a new connector
ConnectorFactory.register("new_provider", NewProviderConnector)

# Create a connector instance
connector = ConnectorFactory.create("gmail", "user@example.com")

# Get available connectors
connectors = ConnectorFactory.get_available_connectors()
```

## 🔐 OAuth Flow

### 1. Get Authorization URL
```bash
curl "http://127.0.0.1:8081/api/v1/unified/auth/google/url"
```

### 2. Handle Callback
```bash
curl "http://127.0.0.1:8081/api/v1/unified/auth/google/callback?code=AUTH_CODE&state=STATE"
```

### 3. Use Connectors
```bash
# List Gmail emails
curl "http://127.0.0.1:8081/api/v1/unified/gmail/emails?user_email=user@example.com"

# List Slack channels
curl "http://127.0.0.1:8081/api/v1/unified/slack/channels?user_email=user@example.com"

# List Jira projects
curl "http://127.0.0.1:8081/api/v1/unified/jira/projects?user_email=user@example.com"
```

## 🧪 Testing

### Run the Test Suite

```bash
# Test the modular structure
python test_modular_oauth.py

# Test with server running
python -m app.main &
python test_modular_oauth.py
```

### Manual Testing

1. **Start the server:**
   ```bash
   python -m app.main
   ```

2. **Access the API documentation:**
   ```
   http://127.0.0.1:8081/docs
   ```

3. **Test OAuth flows:**
   - Get auth URLs for each provider
   - Complete OAuth flows
   - Test connector operations

## 🔄 Adding New Providers

### 1. Create Provider Implementation

```python
# app/providers/new_provider/auth.py
class NewProviderOAuthProvider(OAuthProvider):
    def __init__(self):
        super().__init__("new_provider")
        # Configure provider-specific settings
    
    def get_auth_url(self, state=None, scopes=None):
        # Implement OAuth URL generation
    
    async def handle_callback(self, code, state):
        # Implement OAuth callback handling
```

### 2. Create Connector Implementation

```python
# app/connectors/new_provider/new_provider_connector.py
class NewProviderConnector(DataConnector):
    def __init__(self, user_email):
        super().__init__("new_provider", user_email)
    
    async def list_items(self, **kwargs):
        # Implement item listing
    
    async def get_item(self, item_id, **kwargs):
        # Implement item retrieval
```

### 3. Register with Services

```python
# app/services/oauth_service.py
self.providers["new_provider"] = new_provider_instance

# app/connectors/__init__.py
ConnectorFactory.register("new_provider", NewProviderConnector)
```

## 📊 Monitoring and Logging

### Activity Logging

All operations are logged to the database:

```python
await db_manager.log_activity(
    user_email="user@example.com",
    provider="gmail",
    action="list_emails",
    details={"count": 25}
)
```

### Connection Testing

```bash
# Test connection for a provider
curl "http://127.0.0.1:8081/api/v1/unified/connectors/gmail/test?user_email=user@example.com"
```

## 🚨 Error Handling

The system provides comprehensive error handling:

- **OAuth Errors**: Invalid tokens, expired tokens, configuration issues
- **Connector Errors**: API failures, network issues, rate limiting
- **Database Errors**: Connection issues, data corruption
- **Validation Errors**: Invalid parameters, missing required fields

## 🔒 Security Features

- **Token Management**: Secure storage and refresh of OAuth tokens
- **State Validation**: CSRF protection for OAuth flows
- **Scope Management**: Granular permission control
- **Activity Logging**: Audit trail for all operations
- **Error Sanitization**: Safe error messages in production

## 📈 Performance

- **Connection Pooling**: Reuse HTTP connections
- **Token Caching**: Minimize token refresh operations
- **Async Operations**: Non-blocking I/O for all operations
- **Database Optimization**: Efficient queries and indexing

## 🎯 Integration with Agent Builder

The modular structure enables easy integration with the agent builder:

1. **OAuth Flows**: Seamless authentication for multiple providers
2. **Data Access**: Unified interface for all data sources
3. **Real-time Operations**: Live data retrieval and updates
4. **Error Recovery**: Robust error handling and retry logic

## 📝 Configuration Reference

### Environment Variables

```env
# Server Configuration
HOST=127.0.0.1
PORT=8081
DEBUG=false

# Database
DATABASE_PATH=oauth_tokens.db

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# OAuth Providers
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8081/auth/google/callback

SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret
SLACK_REDIRECT_URI=http://127.0.0.1:8081/auth/slack/callback

ATLASSIAN_CLIENT_ID=your_atlassian_client_id
ATLASSIAN_CLIENT_SECRET=your_atlassian_client_secret
ATLASSIAN_REDIRECT_URI=http://127.0.0.1:8081/auth/atlassian/callback
```

## 🤝 Contributing

1. Follow the modular architecture pattern
2. Add comprehensive tests for new features
3. Update documentation for new providers
4. Ensure backward compatibility
5. Follow the established error handling patterns

## 📄 License

This project is part of the Lagentry AI platform and follows the same licensing terms.

---

**🎉 The modular OAuth backend is now ready for production use with multiple providers!** 