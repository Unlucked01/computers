from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pc_configurator"
    DATABASE_HOST: Optional[str] = "localhost"
    DATABASE_PORT: Optional[int] = 5432
    DATABASE_USER: Optional[str] = "postgres"
    DATABASE_PASSWORD: Optional[str] = "postgres"
    DATABASE_NAME: Optional[str] = "pc_configurator"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://unl-computers.duckdns.org",
        "https://unl-events.duckdns.org"
    ]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # PDF Generation
    PDF_TEMP_PATH: str = "/tmp/pc_configs"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Читаем CORS_ORIGINS из переменной окружения если она есть
        cors_env = os.getenv("CORS_ORIGINS")
        if cors_env:
            # Парсим строку как список, разделенный запятыми
            self.CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",")]
    
    class Config:
        env_file = ".env"
        # Разрешаем дополнительные поля для большей гибкости
        extra = "allow"


settings = Settings() 