from wsgiref.simple_server import make_server
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import traceback

print("=== Debug WSGI Server ===")

try:
    print("1. Creating FastAPI app...")
    app = FastAPI()
    
    @app.get("/")
    def root():
        return {"message": "Debug test working!"}
    
    print("2. Converting to WSGI...")
    wsgi_app = WSGIMiddleware(app)
    
    print("3. Creating server...")
    httpd = make_server('', 8007, wsgi_app)
    
    print("4. Starting server...")
    print("Server will be available at: http://127.0.0.1:8007")
    httpd.serve_forever()
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc() 