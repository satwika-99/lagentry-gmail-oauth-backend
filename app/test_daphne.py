import daphne.server
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Daphne test!"}

if __name__ == "__main__":
    print("Starting Daphne server...")
    print("Server will be available at: http://127.0.0.1:8033")
    
    # Run with daphne
    daphne.server.run(app, host="127.0.0.1", port=8033) 