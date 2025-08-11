## Project Setup Guide

This guide walks you through running the full stack locally:
- FastAPI backend (`app_new`) on port 8081
- n8n workflow automation on port 5678
- Vite + React frontend under `frontend/` on the default Vite port

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+ and pip
- Git
- Docker

---

## 1) Environment Configuration

- **Frontend env**: copy `frontend/env.example` to `frontend/.env` and fill values
- **Backend env**: create `app_new/.env` for FastAPI

### 1.1 `frontend/.env`
Create `.env` for the frontend:

```bash
cp frontend/env.example frontend/.env
```
Update the values:

```bash
# OpenAI key
VITE_OPENAI_API_KEY=your_openai_key

# n8n instance URL (dev default)
VITE_N8N_BASE_URL=http://localhost:5678

# n8n personal access token from n8n UI (Settings → API)
VITE_N8N_API_KEY=your_n8n_api_key

# FastAPI backend URL
VITE_BACKEND_URL=http://localhost:8081
```

Notes:
- The dev server proxies '/n8n-api' to http://localhost:5678 (see frontend/vite.config.ts). Setting VITE_N8N_BASE_URL lets you call n8n directly when needed.
- Do not commit secrets. .env is gitignored.

### 1.2 Backend app_new/.env (FastAPI)
Create a file at app_new/.env:

```bash
# Server
HOST=127.0.0.1
PORT=8081

# Database
DATABASE_PATH=oauth_tokens.db

# CORS (include your frontend port)
CORS_ORIGINS=["http://localhost:5176","http://127.0.0.1:5176","http://localhost:5173","http://127.0.0.1:5173"]

# Google OAuth (optional for testing; required for real OAuth flows)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8081/auth/google/callback

# Slack OAuth (optional)
SLACK_CLIENT_ID=
SLACK_CLIENT_SECRET=
SLACK_REDIRECT_URI=http://127.0.0.1:8081/auth/slack/callback

# Atlassian/Jira OAuth (optional)
ATLASSIAN_CLIENT_ID=
ATLASSIAN_CLIENT_SECRET=
ATLASSIAN_REDIRECT_URI=http://127.0.0.1:8081/auth/atlassian/callback

# Jira API (token-based; optional)
JIRA_INSTANCE_URL=
JIRA_USERNAME=
JIRA_API_TOKEN=

# Misc
SECRET_KEY=change-me
LOG_LEVEL=INFO
DEBUG=true
```

---

## 2) Start n8n (port 5678)
Choose one of the options below.

### Option A: Docker (recommended)
```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n:latest
```

### Option B: Local (npx)
```bash
npx n8n@latest start --port 5678
```

### Create an API token in n8n
1. Open http://localhost:5678
2. Sign up / sign in
3. Go to Settings → API → Create Personal Access Token
4. Copy the token and set VITE_N8N_API_KEY in frontend/.env

---

## 3) Start the FastAPI Backend (port 8081)
From the project root:

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install backend deps
pip install -r app_new/requirements.txt

# Run the backend on 8081
python app_new/run.py
```

Health check and docs:
- http://127.0.0.1:8081/health
- http://127.0.0.1:8081/docs

Notes:
- Backend reads env from app_new/.env (see app_new/core/config.py).
- Alternatively run: python -m uvicorn app_new.main:app --host 127.0.0.1 --port 8081 --reload

---

## 4) Start the Frontend
From the project root:

```bash
cd frontend
npm install
npm run dev --port 5176
```

- Default Vite URL: it will print, usually http://localhost:5176
- Ensure your backend CORS allows your dev port (we included 5176 in CORS_ORIGINS).
- The dev server proxies '/n8n-api' to http://localhost:5678 so you can call n8n without CORS issues.
- Optional: There is an additional OAuth demo UI in frontend/oauth_frontend/ (Create React App). It’s not required for the main app.

---

## 5) Verify Everything Works
- n8n UI: http://localhost:5678
- Backend health: http://127.0.0.1:8081/health
- Backend docs: http://127.0.0.1:8081/docs#
- Frontend: http://localhost:5176

Quick API check (in another terminal):
```bash
curl http://127.0.0.1:8081/health
```
You should see a healthy JSON response.

---

## 6) GitHub: Initialize and Push
From the project root:

```bash
git init
git add .
git commit -m "Initial commit"
# Replace <USER_OR_ORG> and <REPO_NAME>
git branch -M main
git remote add origin git@github.com:<USER_OR_ORG>/<REPO_NAME>.git
git push -u origin main
```

Ensure .env files are not committed (already in .gitignore).

---

## Useful Notes
- Vite proxy for n8n: configured in frontend/vite.config.ts to forward '/n8n-api' → http://localhost:5678.
- Frontend env usage: see frontend/src/config/n8n.ts. You should override defaults via frontend/.env.
- Backend env: app_new/core/config.py shows all configurable variables and defaults.
- SQLite: token storage is a local SQLite database (default app_new/oauth_tokens.db).

---

## Database (SQLite)
- The backend uses SQLite for local development and automatically creates DB files on first run.
- Default locations you may see:
  - app_new/oauth_tokens.db (backend tokens DB)
  - oauth_tokens.db (legacy/dev DB)
- No manual setup is required for local dev.
- These files are ignored by Git. To reset the DB, stop the backend and delete the DB files; they will be recreated on next start.
- For production, use a managed database and set DATABASE_PATH in app_new/.env accordingly.

---

## Troubleshooting
- Port already in use:
  - n8n (5678): change or stop the conflicting process.
  - Backend (8081): change PORT in app_new/.env and update VITE_BACKEND_URL accordingly.
- CORS errors: ensure your frontend URL is included in CORS_ORIGINS in app_new/.env.
- 401 calling n8n: verify VITE_N8N_API_KEY and that requests are sent via '/n8n-api' or VITE_N8N_BASE_URL.
- OAuth not redirecting: confirm redirect URIs in provider consoles match your backend URLs on port 8081.

---

## Project Structure (high level)
- app_new/: FastAPI backend (OAuth providers, API, storage)
- frontend/: Vite + React frontend
- frontend/oauth_frontend/: Optional demo OAuth UI (CRA)
- frontend/env.example: Template for frontend/.env
- frontend/vite.config.ts: Dev proxy to n8n (5678)
- app_new/run.py: Starts FastAPI on 8081