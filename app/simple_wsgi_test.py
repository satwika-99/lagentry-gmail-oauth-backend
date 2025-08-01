from wsgiref.simple_server import make_server
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Simple test working!"}

@app.get("/test")
def test():
    return {"status": "ok"}

# Convert FastAPI to WSGI
wsgi_app = WSGIMiddleware(app)

if __name__ == "__main__":
    print("Starting simple WSGI test...")
    print("Server will be available at: http://127.0.0.1:8006")
    
    with make_server('', 8006, wsgi_app) as httpd:
        print("Serving at port 8006...")
        httpd.serve_forever() 