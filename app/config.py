import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Notes API"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/notes_db")

    class Config:
        env_file = ".env"

settings = Settings()
