from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from src.presentation.api.user_routes import router as user_router
from src.presentation.api.todo_routes import router as todo_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo App API",
        description="Simple Todo App with Layered Architecture",
        version="1.0.0"
    )
    
    # Configure CORS based on environment
    is_production = os.getenv("RENDER") is not None
    allowed_origins = ["*"] if not is_production else [
        "https://your-frontend-domain.com",  # Replace with your actual frontend domain
        "http://localhost:3000",  # For local development
        "http://localhost:8080",  # For local development
    ]
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(user_router, prefix="/api")
    app.include_router(todo_router, prefix="/api")
    
    @app.get("/")
    async def root():
        return {"message": "Todo App API is running!"}
    
    @app.get("/health")
    async def health_check():
        try:
            # Try to import database connection to verify it's working
            from src.infrastructure.database.connection import engine
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
        except Exception as e:
            return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
    
    return app


app = create_app()