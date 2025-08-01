import hypercorn.asyncio
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hypercorn test!"}

async def main():
    config = hypercorn.Config()
    config.bind = ["127.0.0.1:8024"]
    config.worker_class = "asyncio"
    await hypercorn.asyncio.serve(app, config)

if __name__ == "__main__":
    print("Starting Hypercorn server...")
    print("Server will be available at: http://127.0.0.1:8024")
    asyncio.run(main()) 