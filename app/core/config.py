import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Общие настройки
    PROJECT_NAME: str = "Notes API"
    DEBUG: bool = Field(default=False)

    # База данных
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field(..., env='POSTGRES_DB')
    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST', default='localhost')
    POSTGRES_PORT: int = Field(default=5432)

    # SQLAlchemy Database URL
    SQLALCHEMY_DATABASE_URL: str = Field(init=False)

    # JWT секрет и алгоритм
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Логирование
    LOG_LEVEL: str = "INFO"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SQLALCHEMY_DATABASE_URL = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
