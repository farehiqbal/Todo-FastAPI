from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database
    database_url: str = Field(default="postgresql+asyncpg://postgres:password@localhost:5432/todo_db")
    database_host: str = Field(default="localhost")
    database_port: int = Field(default=5432)
    database_name: str = Field(default="todo")
    database_user: str = Field(default="postgres")
    database_password: str = Field(default="soap")
    
    # JWT
    jwt_secret_key: str = Field(default="fallback-secret-key")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)
    
    # App
    app_name: str = Field(default="Todo App")
    app_version: str = Field(default="1.0.0")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    debug: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()