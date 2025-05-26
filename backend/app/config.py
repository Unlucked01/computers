from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, List, Union
import json


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pc_configurator"
    DATABASE_HOST: Optional[str] = "localhost"
    DATABASE_PORT: Optional[int] = 5432
    DATABASE_USER: Optional[str] = "postgres"
    DATABASE_PASSWORD: Optional[str] = "postgres"
    DATABASE_NAME: Optional[str] = "pc_configurator"

    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    PDF_TEMP_PATH: str = "/tmp/pc_configs"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)  # JSON-строка?
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
