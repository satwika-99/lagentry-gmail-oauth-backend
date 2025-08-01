import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Alternative server test!"}

if __name__ == "__main__":
    print("Starting alternative server...")
    print("Server will be available at: http://127.0.0.1:8023")
    
    # Try different uvicorn settings
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8023,
        log_level="info",
        reload=False,
        loop="asyncio",
        access_log=True,
        use_colors=False
    ) 