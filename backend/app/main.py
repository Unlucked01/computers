from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import engine, Base
from .routers import components, configurations, categories
import os

app = FastAPI(
    title="Конфигуратор ПК API",
    description="API для веб-конфигуратора персональных компьютеров",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание директории для PDF файлов
os.makedirs(settings.PDF_TEMP_PATH, exist_ok=True)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение роутеров
app.include_router(categories.router, prefix="/api/v1", tags=["Категории"])
app.include_router(components.router, prefix="/api/v1", tags=["Компоненты"])
app.include_router(configurations.router, prefix="/api/v1", tags=["Конфигурации"])


@app.get("/")
async def root():
    """Главная страница API"""
    return {
        "message": "Конфигуратор ПК API", 
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "ok", "environment": settings.ENVIRONMENT} 