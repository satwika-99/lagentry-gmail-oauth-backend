from wsgiref.simple_server import make_server
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

app = FastAPI()

@app.get("/")
def root():
    return {"message": "WSGI test!"}

# Convert FastAPI to WSGI
wsgi_app = WSGIMiddleware(app)

if __name__ == "__main__":
    print("Starting WSGI server...")
    print("Server will be available at: http://127.0.0.1:8034")
    
    with make_server('', 8034, wsgi_app) as httpd:
        print("Serving at port 8034...")
        httpd.serve_forever() 