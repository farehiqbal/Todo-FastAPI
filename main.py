import os
import uvicorn
from src.presentation.app import app
from src.infrastructure.config.settings import settings

# Expose the app at module level for production servers
app = app

if __name__ == "__main__":
    port = int(os.getenv("PORT", settings.app_port))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )