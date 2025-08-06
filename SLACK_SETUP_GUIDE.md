# Slack Integration Setup Guide

## Why You Don't See Real Messages

Currently, the system is using **mock data** for testing purposes. The messages you see in the tests are simulated responses, not actual Slack messages. To send real messages to your Slack workspace, you need to set up proper OAuth credentials.

## Step 1: Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter app name (e.g., "Lagentry Backend")
5. Select your workspace: **T098ENSU7DM**

## Step 2: Configure OAuth Settings

1. In your Slack app dashboard, go to **"OAuth & Permissions"**
2. Add these **Redirect URLs**:
   - `http://localhost:8083/auth/slack/callback`
   - `http://127.0.0.1:8083/auth/slack/callback`

## Step 3: Add Required Scopes

Under **"Scopes"** → **"Bot Token Scopes"**, add:
- `channels:read`
- `channels:history`
- `chat:write`
- `users:read`
- `users:read.email`

## Step 4: Install App to Workspace

1. Go to **"Install App"** in the sidebar
2. Click **"Install to Workspace"**
3. Authorize the app

## Step 5: Get Your Credentials

After installation, you'll get:
- **Client ID** (starts with your app ID)
- **Client Secret** (starts with `xoxb-`)

## Step 6: Update Environment Variables

Update your `.env` file with real credentials:

```env
# Slack OAuth Configuration
SLACK_CLIENT_ID=your_actual_slack_client_id
SLACK_CLIENT_SECRET=your_actual_slack_client_secret
SLACK_REDIRECT_URI=http://localhost:8083/auth/slack/callback
```

## Step 7: Test Real Integration

Once configured, run:

```bash
py test_slack_workspace.py
```

## Current Status

**❌ Mock Data Mode (Current)**
- Messages are simulated
- No real Slack API calls
- Good for testing endpoints

**✅ Real Integration Mode (After Setup)**
- Real messages sent to Slack
- Actual API calls to Slack
- Messages appear in your workspace

## Quick Test

To verify if you have real credentials configured:

```bash
py -c "
import os
from app.core.config import settings
print(f'Slack Client ID: {settings.slack_client_id}')
print(f'Slack Client Secret: {settings.slack_client_secret[:10] if settings.slack_client_secret else \"Not set\"}')
"
```

If you see "your_slack_client_id_here", you're still in mock mode.

## Need Help?

1. **Slack App Creation**: Follow the official guide at [api.slack.com](https://api.slack.com/apps)
2. **OAuth Setup**: See [Slack OAuth documentation](https://api.slack.com/authentication/oauth-v2)
3. **Permissions**: Ensure your app has the required scopes

Once you set up the real credentials, the messages will actually appear in your Slack workspace at `https://app.slack.com/client/T098ENSU7DM/C098WCB0362`! 