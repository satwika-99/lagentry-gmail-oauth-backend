import http.server
import socketserver
import json
import urllib.parse
import asyncio
from urllib.parse import urlparse, parse_qs
from config import config
from storage import init_db, get_all_users, store_tokens, get_valid_tokens
from auth import generate_auth_url, handle_oauth_callback, get_access_token_for_user
from gmail import fetch_emails, fetch_email_content, search_emails

# Initialize database
init_db()

class GmailOAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        try:
            if path == '/':
                response = {"message": "Gmail OAuth Backend is running!"}
                self.send_json_response(200, response)
                
            elif path == '/auth/google':
                auth_url = generate_auth_url()
                self.send_response(302)
                self.send_header('Location', auth_url)
                self.end_headers()
                
            elif path == '/auth/google/callback':
                code = query_params.get('code', [None])[0]
                state = query_params.get('state', [None])[0]
                
                if code and state:
                    # Run async function in sync context
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        result = loop.run_until_complete(handle_oauth_callback(code, state))
                        self.send_json_response(200, result)
                    finally:
                        loop.close()
                else:
                    self.send_json_response(400, {"error": "Missing code or state parameter"})
                    
            elif path == '/emails':
                user_email = query_params.get('user_email', [None])[0]
                max_results = int(query_params.get('max_results', [10])[0])
                
                if user_email:
                    # Run async function in sync context
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        emails = loop.run_until_complete(fetch_emails(user_email, max_results))
                        self.send_json_response(200, emails)
                    finally:
                        loop.close()
                else:
                    self.send_json_response(400, {"error": "Missing user_email parameter"})
                    
            elif path.startswith('/emails/'):
                message_id = path.split('/')[-1]
                user_email = query_params.get('user_email', [None])[0]
                
                if user_email and message_id:
                    # Run async function in sync context
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        content = loop.run_until_complete(fetch_email_content(user_email, message_id))
                        self.send_json_response(200, content)
                    finally:
                        loop.close()
                else:
                    self.send_json_response(400, {"error": "Missing user_email or message_id"})
                    
            elif path == '/emails/search':
                user_email = query_params.get('user_email', [None])[0]
                query = query_params.get('query', [None])[0]
                max_results = int(query_params.get('max_results', [10])[0])
                
                if user_email and query:
                    # Run async function in sync context
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        results = loop.run_until_complete(search_emails(user_email, query, max_results))
                        self.send_json_response(200, results)
                    finally:
                        loop.close()
                else:
                    self.send_json_response(400, {"error": "Missing user_email or query parameter"})
                    
            elif path == '/users':
                users = get_all_users()
                self.send_json_response(200, {"users": users})
                
            else:
                self.send_json_response(404, {"error": "Endpoint not found"})
                
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    print("Starting Gmail OAuth Backend...")
    print("Server will be available at: http://127.0.0.1:8010")
    print("Available endpoints:")
    print("  GET / - Server status")
    print("  GET /auth/google - Start OAuth flow")
    print("  GET /auth/google/callback - OAuth callback")
    print("  GET /emails?user_email=... - Fetch emails")
    print("  GET /emails/{message_id}?user_email=... - Get email content")
    print("  GET /emails/search?user_email=...&query=... - Search emails")
    print("  GET /users - List all users")
    print("Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(('', 8010), GmailOAuthHandler) as httpd:
        print("Serving at port 8010...")
        httpd.serve_forever() 