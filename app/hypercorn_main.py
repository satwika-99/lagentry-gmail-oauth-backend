import hypercorn.asyncio
import asyncio
from main import app

async def main():
    config = hypercorn.Config()
    config.bind = ["127.0.0.1:8005"]
    config.worker_class = "asyncio"
    print("Starting Gmail OAuth Backend with Hypercorn...")
    print("Server will be available at: http://127.0.0.1:8005")
    await hypercorn.asyncio.serve(app, config)

if __name__ == "__main__":
    asyncio.run(main()) 