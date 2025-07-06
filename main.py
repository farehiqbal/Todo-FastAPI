import uvicorn
from src.presentation.app import app
from src.infrastructure.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )