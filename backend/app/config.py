from pydantic_settings import BaseSettings
from typing import Optional


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
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # PDF Generation
    PDF_TEMP_PATH: str = "/tmp/pc_configs"
    
    class Config:
        env_file = ".env"
        # Разрешаем дополнительные поля для большей гибкости
        extra = "allow"


settings = Settings() 