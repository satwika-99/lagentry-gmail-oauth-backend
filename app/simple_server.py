import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting Gmail OAuth Backend...")
    print("Server will be available at: http://127.0.0.1:8019")
    uvicorn.run(app, host="127.0.0.1", port=8019, log_level="info", reload=False) 