"""
Main FastAPI application for the Lagentry OAuth Backend
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from .core.config import settings
from .core.database import db_manager
from .core.auth import validate_google_config
from .api.v1 import auth, google


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting Lagentry OAuth Backend...")
    
    # Initialize database
    try:
        db_manager.init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    
    # Validate configurations
    try:
        validate_google_config()
        print("✅ Google OAuth configuration validated")
    except Exception as e:
        print(f"⚠️  Google OAuth not configured: {e}")
    
    print(f"🌐 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"📚 API Documentation: http://{settings.host}:{settings.port}/docs")
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Lagentry OAuth Backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Custom OAuth 2.0 backend for Lagentry AI agents",
    version=settings.app_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(google.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "auth": "/api/v1/auth",
            "google": "/api/v1/google",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version
    }


@app.get("/api/v1/emails")
async def get_emails(user_email: str, max_results: int = 10):
    """Legacy endpoint for backward compatibility"""
    try:
        from .providers.google.gmail import gmail_service
        result = await gmail_service.get_user_emails(user_email, max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch emails: {str(e)}")


@app.get("/api/v1/users")
async def get_users():
    """Legacy endpoint for backward compatibility"""
    try:
        users = db_manager.get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "details": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import httpx
    from datetime import datetime
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 