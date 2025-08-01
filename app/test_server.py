#!/usr/bin/env python3
"""
Simple test server to check if uvicorn works
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Test server is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting test server...")
    print("Server will be available at: http://127.0.0.1:8011")
    uvicorn.run(app, host="127.0.0.1", port=8011, log_level="info") 