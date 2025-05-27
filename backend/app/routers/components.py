from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from ..database import get_db
from ..models import Component, ComponentCategory, ComponentStock
from ..schemas.component import ComponentResponse, ComponentFilter
from ..schemas.configuration import CompatibilityCheck
from ..services.compatibility_service import CompatibilityService
import uuid

router = APIRouter()


@router.get("/components", response_model=List[ComponentResponse])
async def get_components(
    category_slug: Optional[str] = Query(None, description="Фильтр по категории"),
    brand: Optional[List[str]] = Query(None, description="Фильтр по брендам"),
    price_min: Optional[float] = Query(None, description="Минимальная цена"),
    price_max: Optional[float] = Query(None, description="Максимальная цена"),
    only_in_stock: bool = Query(False, description="Только товары в наличии"),
    form_factor: Optional[List[str]] = Query(None, description="Фильтр по форм-фактору"),
    power_max: Optional[int] = Query(None, description="Максимальное энергопотребление"),
    search: Optional[str] = Query(None, description="Поиск по названию/модели"),
    socket: Optional[List[str]] = Query(None, description="Фильтр по сокету"),
    memory_type: Optional[List[str]] = Query(None, description="Фильтр по типу памяти"),
    interface: Optional[List[str]] = Query(None, description="Фильтр по интерфейсу"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество на странице"),
    db: Session = Depends(get_db)
):
    """Получить компоненты с фильтрацией"""
    
    query = db.query(Component).options(
        joinedload(Component.category),
        joinedload(Component.stock)
    ).filter(Component.is_active == True)
    
    # Фильтр по категории
    if category_slug:
        query = query.join(ComponentCategory).filter(ComponentCategory.slug == category_slug)
    
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
    
    # Фильтр по форм-фактору
    if form_factor:
        query = query.filter(Component.form_factor.in_(form_factor))
    
    # Фильтр по энергопотреблению
    if power_max is not None:
        query = query.filter(
            or_(
                Component.power_consumption <= power_max,
                Component.power_consumption.is_(None)
            )
        )
    
    # Поиск по тексту
    if search:
        search_filter = or_(
            Component.name.ilike(f"%{search}%"),
            Component.model.ilike(f"%{search}%"),
            Component.brand.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Фильтр по сокету (для процессоров/материнок)
    if socket:
        query = query.filter(Component.specifications["socket"].astext.in_(socket))
    
    # Фильтр по типу памяти
    if memory_type:
        query = query.filter(Component.specifications["memory_type"].astext.in_(memory_type))
    
    # Фильтр по интерфейсу
    if interface:
        query = query.filter(Component.specifications["interface"].astext.in_(interface))
    
    # Пагинация
    offset = (page - 1) * limit
    components = query.offset(offset).limit(limit).all()
    
    return components


@router.get("/components/{component_id}", response_model=ComponentResponse)
async def get_component(component_id: str, db: Session = Depends(get_db)):
    """Получить компонент по ID"""
    component = db.query(Component).options(
        joinedload(Component.category),
        joinedload(Component.stock)
    ).filter(Component.id == component_id).first()
    
    if not component:
        raise HTTPException(status_code=404, detail="Компонент не найден")
    
    return component


@router.get("/components/category/{category_slug}", response_model=List[ComponentResponse])
async def get_components_by_category(
    category_slug: str,
    brand: Optional[List[str]] = Query(None, description="Фильтр по брендам"),
    price_min: Optional[float] = Query(None, description="Минимальная цена"),
    price_max: Optional[float] = Query(None, description="Максимальная цена"),
    only_in_stock: bool = Query(False, description="Только товары в наличии"),
    form_factor: Optional[List[str]] = Query(None, description="Фильтр по форм-фактору"),
    power_max: Optional[int] = Query(None, description="Максимальное энергопотребление"),
    search: Optional[str] = Query(None, description="Поиск по названию/модели"),
    socket: Optional[List[str]] = Query(None, description="Фильтр по сокету"),
    memory_type: Optional[List[str]] = Query(None, description="Фильтр по типу памяти"),
    interface: Optional[List[str]] = Query(None, description="Фильтр по интерфейсу"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество на странице"),
    compatible_with: Optional[List[str]] = Query(None, description="ID компонентов для проверки совместимости"),
    db: Session = Depends(get_db)
):
    """Получить компоненты категории с фильтрацией и поиском"""
    
    # Проверяем существование категории
    category = db.query(ComponentCategory).filter(ComponentCategory.slug == category_slug).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    query = db.query(Component).options(
        joinedload(Component.category),
        joinedload(Component.stock)
    ).filter(
        Component.category_id == category.id,
        Component.is_active == True
    )
    
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
    
    # Фильтр по форм-фактору
    if form_factor:
        query = query.filter(Component.form_factor.in_(form_factor))
    
    # Фильтр по энергопотреблению
    if power_max is not None:
        query = query.filter(
            or_(
                Component.power_consumption <= power_max,
                Component.power_consumption.is_(None)
            )
        )
    
    # Поиск по тексту
    if search:
        search_filter = or_(
            Component.name.ilike(f"%{search}%"),
            Component.model.ilike(f"%{search}%"),
            Component.brand.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Фильтр по сокету (для процессоров/материнок)
    if socket:
        query = query.filter(Component.specifications["socket"].astext.in_(socket))
    
    # Фильтр по типу памяти
    if memory_type:
        query = query.filter(Component.specifications["memory_type"].astext.in_(memory_type))
    
    # Фильтр по интерфейсу
    if interface:
        query = query.filter(Component.specifications["interface"].astext.in_(interface))
    
    # Пагинация
    offset = (page - 1) * limit
    components = query.offset(offset).limit(limit).all()
    
    # Если нужна проверка совместимости
    if compatible_with:
        compatibility_service = CompatibilityService(db)
        compatible_components = []
        
        for component in components:
            test_config = compatible_with + [str(component.id)]
            compatibility = compatibility_service.check_configuration_compatibility(test_config)
            
            # Добавляем только совместимые компоненты или с предупреждениями
            if compatibility.status in ["compatible", "warning"]:
                compatible_components.append(component)
        
        components = compatible_components
    
    return components


@router.post("/components/check-compatibility", response_model=CompatibilityCheck)
async def check_components_compatibility(
    component_ids: List[str],
    db: Session = Depends(get_db)
):
    """Проверить совместимость набора компонентов"""
    if not component_ids:
        raise HTTPException(status_code=400, detail="Список компонентов не может быть пустым")
    
    # Валидация UUID формата
    invalid_uuids = []
    for comp_id in component_ids:
        try:
            uuid.UUID(comp_id)
        except ValueError:
            invalid_uuids.append(comp_id)
    
    if invalid_uuids:
        raise HTTPException(
            status_code=400,
            detail=f"Некорректный формат UUID: {invalid_uuids}"
        )
    
    # Проверяем существование всех компонентов
    existing_components = db.query(Component.id).filter(Component.id.in_(component_ids)).all()
    existing_ids = {str(comp.id) for comp in existing_components}
    missing_ids = set(component_ids) - existing_ids
    
    if missing_ids:
        # Получаем информацию о существующих компонентах для отладки
        existing_count = len(existing_ids)
        total_components = db.query(Component).count()
        
        raise HTTPException(
            status_code=404, 
            detail={
                "message": "Компоненты не найдены",
                "missing_ids": list(missing_ids),
                "existing_count": existing_count,
                "total_components_in_db": total_components,
                "requested_ids": component_ids
            }
        )
    
    compatibility_service = CompatibilityService(db)
    result = compatibility_service.check_configuration_compatibility(component_ids)
    
    return result


@router.get("/components/debug/ids")
async def get_all_component_ids(db: Session = Depends(get_db)):
    """Получить все ID компонентов для отладки"""
    components = db.query(Component.id, Component.name, Component.brand, Component.is_active).all()
    
    return {
        "total_count": len(components),
        "active_count": len([c for c in components if c.is_active]),
        "components": [
            {
                "id": str(comp.id),
                "name": comp.name,
                "brand": comp.brand,
                "is_active": comp.is_active
            }
            for comp in components
        ]
    }


@router.get("/components/filters/options")
async def get_filter_options(
    category_slug: Optional[str] = Query(None, description="Категория для фильтров"),
    db: Session = Depends(get_db)
):
    """Получить доступные варианты для фильтров"""
    
    query = db.query(Component).filter(Component.is_active == True)
    
    if category_slug:
        query = query.join(ComponentCategory).filter(ComponentCategory.slug == category_slug)
    
    components = query.all()
    
    # Собираем уникальные значения для фильтров
    brands = list(set(comp.brand for comp in components if comp.brand))
    form_factors = list(set(comp.form_factor for comp in components if comp.form_factor))
    
    # Специфичные фильтры из specifications
    sockets = set()
    memory_types = set()
    interfaces = set()
    
    for comp in components:
        specs = comp.specifications or {}
        
        if "socket" in specs:
            sockets.add(specs["socket"])
        if "memory_type" in specs:
            if isinstance(specs["memory_type"], list):
                memory_types.update(specs["memory_type"])
            else:
                memory_types.add(specs["memory_type"])
        if "interface" in specs:
            interfaces.add(specs["interface"])
    
    return {
        "brands": sorted(brands),
        "form_factors": sorted(form_factors),
        "sockets": sorted(list(sockets)),
        "memory_types": sorted(list(memory_types)),
        "interfaces": sorted(list(interfaces)),
        "price_range": {
            "min": min((comp.price for comp in components), default=0),
            "max": max((comp.price for comp in components), default=0)
        }
    } 