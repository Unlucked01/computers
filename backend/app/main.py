from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from .config import settings
from .database import engine, Base
from .routers import components, configurations, categories, accessories
import os
import logging
import time
import traceback

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Логируем входящий запрос
    logger.info(f"🔵 {request.method} {request.url}")
    
    # Выполняем запрос
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Логируем ответ
        if response.status_code >= 400:
            logger.error(f"🔴 {request.method} {request.url} - {response.status_code} ({process_time:.3f}s)")
        else:
            logger.info(f"🟢 {request.method} {request.url} - {response.status_code} ({process_time:.3f}s)")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"💥 {request.method} {request.url} - ERROR ({process_time:.3f}s): {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Внутренняя ошибка сервера: {str(e)}"}
        )

# Создание директории для PDF файлов
os.makedirs(settings.PDF_TEMP_PATH, exist_ok=True)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение роутеров
app.include_router(categories.router, prefix="/api/v1", tags=["Категории"])
app.include_router(components.router, prefix="/api/v1", tags=["Компоненты"])
app.include_router(configurations.router, prefix="/api/v1", tags=["Конфигурации"])
app.include_router(accessories.router, prefix="/api/v1", tags=["Аксессуары"])

# Добавляем роутеры без префикса для совместимости с фронтендом
app.include_router(categories.router, tags=["Категории (без префикса)"])
app.include_router(components.router, tags=["Компоненты (без префикса)"])
app.include_router(configurations.router, tags=["Конфигурации (без префикса)"])
app.include_router(accessories.router, tags=["Аксессуары (без префикса)"])

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