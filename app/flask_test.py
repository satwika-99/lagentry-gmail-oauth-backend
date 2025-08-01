from flask import Flask, jsonify
from wsgiref.simple_server import make_server

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({"message": "Flask test working!"})

@app.route('/test')
def test():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("Starting Flask test...")
    print("Server will be available at: http://127.0.0.1:8008")
    
    with make_server('', 8008, app) as httpd:
        print("Serving at port 8008...")
        httpd.serve_forever() 