"""
FastAPI main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.db import create_db_and_tables
from app.api.tasks import router as tasks_router

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="RESTful API for Todo application with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

# Support Vercel preview deployments with regex pattern
# This allows all Vercel preview URLs (*.vercel.app) while keeping specific origins secure
allow_origin_regex = os.getenv("CORS_ALLOW_ORIGIN_REGEX", r"https://.*\.vercel\.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event: Create database tables
@app.on_event("startup")
def on_startup():
    """
    Create database tables on application startup.
    In production, use migrations (e.g., Alembic) instead.
    """
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully.")


# Include routers
app.include_router(tasks_router, tags=["tasks"])


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint for health check.
    """
    return {
        "message": "Todo API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
