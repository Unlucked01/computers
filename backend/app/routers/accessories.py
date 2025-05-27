from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from ..database import get_db
from ..models import Component, ComponentCategory, ComponentStock
from ..schemas.component import ComponentResponse, ComponentFilter

router = APIRouter()


@router.get("/accessories", response_model=List[ComponentResponse])
async def get_accessories(
    type_filter: Optional[List[str]] = Query(None, description="Фильтр по типу аксессуара"),
    brand: Optional[List[str]] = Query(None, description="Фильтр по брендам"),
    price_min: Optional[float] = Query(None, description="Минимальная цена"),
    price_max: Optional[float] = Query(None, description="Максимальная цена"),
    only_in_stock: bool = Query(False, description="Только товары в наличии"),
    connection: Optional[List[str]] = Query(None, description="Фильтр по типу подключения"),
    search: Optional[str] = Query(None, description="Поиск по названию/модели"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество на странице"),
    db: Session = Depends(get_db)
):
    """Получить аксессуары с фильтрацией"""
    
    # Получаем категорию аксессуаров
    accessories_category = db.query(ComponentCategory).filter(
        ComponentCategory.slug == "accessories"
    ).first()
    
    if not accessories_category:
        raise HTTPException(status_code=404, detail="Категория аксессуаров не найдена")
    
    query = db.query(Component).options(
        joinedload(Component.category),
        joinedload(Component.stock)
    ).filter(
        Component.category_id == accessories_category.id,
        Component.is_active == True
    )
    
    # Фильтр по типу аксессуара
    if type_filter:
        query = query.filter(Component.specifications["type"].astext.in_(type_filter))
    
    # Фильтр по бренду
    if brand:
        query = query.filter(Component.brand.in_(brand))
    
    # Фильтр по цене
    if price_min is not None:
        query = query.filter(Component.price >= price_min)
    if price_max is not None:
        query = query.filter(Component.price <= price_max)
    
    # Фильтр по наличию
    if only_in_stock:
        query = query.join(ComponentStock).filter(ComponentStock.status == "in_stock")
    
    # Фильтр по типу подключения
    if connection:
        query = query.filter(Component.specifications["connection"].astext.in_(connection))
    
    # Поиск по тексту
    if search:
        search_filter = or_(
            Component.name.ilike(f"%{search}%"),
            Component.model.ilike(f"%{search}%"),
            Component.brand.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Пагинация
    offset = (page - 1) * limit
    accessories = query.offset(offset).limit(limit).all()
    
    return accessories


@router.get("/accessories/{accessory_id}", response_model=ComponentResponse)
async def get_accessory(accessory_id: str, db: Session = Depends(get_db)):
    """Получить аксессуар по ID"""
    accessory = db.query(Component).options(
        joinedload(Component.category),
        joinedload(Component.stock)
    ).filter(Component.id == accessory_id).first()
    
    if not accessory:
        raise HTTPException(status_code=404, detail="Аксессуар не найден")
    
    # Проверяем, что это действительно аксессуар
    if accessory.category.slug != "accessories":
        raise HTTPException(status_code=400, detail="Компонент не является аксессуаром")
    
    return accessory


@router.get("/accessories/filters/options")
async def get_accessories_filter_options(db: Session = Depends(get_db)):
    """Получить доступные опции для фильтров аксессуаров"""
    
    # Получаем категорию аксессуаров
    accessories_category = db.query(ComponentCategory).filter(
        ComponentCategory.slug == "accessories"
    ).first()
    
    if not accessories_category:
        raise HTTPException(status_code=404, detail="Категория аксессуаров не найдена")
    
    # Получаем все аксессуары для анализа
    accessories = db.query(Component).filter(
        Component.category_id == accessories_category.id,
        Component.is_active == True
    ).all()
    
    # Собираем уникальные значения для фильтров
    brands = list(set(acc.brand for acc in accessories))
    types = list(set(acc.specifications.get("type") for acc in accessories if acc.specifications.get("type")))
    connections = list(set(acc.specifications.get("connection") for acc in accessories if acc.specifications.get("connection")))
    
    # Ценовой диапазон
    prices = [acc.price for acc in accessories]
    price_range = {
        "min": min(prices) if prices else 0,
        "max": max(prices) if prices else 0
    }
    
    return {
        "brands": sorted(brands),
        "types": sorted(types),
        "connections": sorted(connections),
        "price_range": price_range
    }


@router.get("/accessories/categories")
async def get_accessories_categories(db: Session = Depends(get_db)):
    """Получить категории аксессуаров (типы)"""
    
    # Получаем категорию аксессуаров
    accessories_category = db.query(ComponentCategory).filter(
        ComponentCategory.slug == "accessories"
    ).first()
    
    if not accessories_category:
        raise HTTPException(status_code=404, detail="Категория аксессуаров не найдена")
    
    # Получаем все типы аксессуаров
    accessories = db.query(Component).filter(
        Component.category_id == accessories_category.id,
        Component.is_active == True
    ).all()
    
    # Группируем по типам
    type_counts = {}
    for acc in accessories:
        acc_type = acc.specifications.get("type")
        if acc_type:
            type_counts[acc_type] = type_counts.get(acc_type, 0) + 1
    
    # Создаем список категорий с русскими названиями
    type_names = {
        "mouse": "Мыши",
        "keyboard": "Клавиатуры", 
        "monitor": "Мониторы",
        "headset": "Гарнитуры",
        "headphones": "Наушники",
        "webcam": "Веб-камеры",
        "mousepad": "Коврики для мыши"
    }
    
    categories = []
    for acc_type, count in type_counts.items():
        categories.append({
            "slug": acc_type,
            "name": type_names.get(acc_type, acc_type.title()),
            "count": count
        })
    
    return sorted(categories, key=lambda x: x["name"]) 