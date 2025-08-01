from wsgiref.simple_server import make_server
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from config import config
from storage import init_db, get_all_users
from auth import generate_auth_url, handle_oauth_callback
from gmail import fetch_emails, fetch_email_content, search_emails

# Initialize the database
init_db()

# Create FastAPI app
app = FastAPI(title="Gmail OAuth Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Gmail OAuth Backend is running!"}

@app.get("/auth/google")
async def google_auth():
    auth_url = generate_auth_url()
    return RedirectResponse(url=auth_url)

@app.get("/auth/google/callback")
async def google_auth_callback(code: str, state: str):
    try:
        result = await handle_oauth_callback(code, state)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/emails")
async def get_emails(user_email: str, max_results: int = 10):
    try:
        emails = await fetch_emails(user_email, max_results)
        return emails
    except Exception as e:
        return {"error": str(e)}

@app.get("/emails/{message_id}")
async def get_email_content(user_email: str, message_id: str):
    try:
        content = await fetch_email_content(user_email, message_id)
        return content
    except Exception as e:
        return {"error": str(e)}

@app.get("/emails/search")
async def search_emails_endpoint(user_email: str, query: str, max_results: int = 10):
    try:
        results = await search_emails(user_email, query, max_results)
        return results
    except Exception as e:
        return {"error": str(e)}

@app.get("/users")
async def get_users():
    try:
        users = get_all_users()
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}

# Convert FastAPI to WSGI
wsgi_app = WSGIMiddleware(app)

if __name__ == "__main__":
    print("Starting Gmail OAuth Backend with WSGI...")
    print("Server will be available at: http://127.0.0.1:8005")
    print("Press Ctrl+C to stop the server")
    
    with make_server('', 8005, wsgi_app) as httpd:
        print("Serving at port 8005...")
        httpd.serve_forever() 