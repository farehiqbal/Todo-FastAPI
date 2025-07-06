from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.user_routes import router as user_router
from src.presentation.api.todo_routes import router as todo_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo App API",
        description="Simple Todo App with Layered Architecture",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
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
        return {"status": "healthy"}
    
    return app


app = create_app()