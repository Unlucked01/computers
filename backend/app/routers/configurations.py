from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid
from datetime import datetime
from uuid import UUID
from ..database import get_db
from ..models import Configuration, ConfigurationItem, Component
from ..schemas.configuration import (
    ConfigurationCreate, ConfigurationResponse, 
    ConfigurationItemCreate, CompatibilityCheck,
    ConfigurationExport
)
from ..services.compatibility_service import CompatibilityService
from ..services.pdf_service import PDFService

router = APIRouter()


@router.post("/configurations", response_model=ConfigurationResponse)
async def create_configuration(
    config_data: ConfigurationCreate,
    db: Session = Depends(get_db)
):
    """Создать новую конфигурацию"""
    db_config = Configuration(
        name=config_data.name,
        description=config_data.description,
        public_uuid=str(uuid.uuid4())
    )
    
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    return db_config


@router.get("/configurations", response_model=List[ConfigurationResponse])
async def get_configurations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список конфигураций"""
    configs = db.query(Configuration).options(
        joinedload(Configuration.items).joinedload(ConfigurationItem.component)
    ).offset(skip).limit(limit).all()
    
    return configs


@router.get("/configurations/{config_id}", response_model=ConfigurationResponse)
async def get_configuration(config_id: UUID, db: Session = Depends(get_db)):
    """Получить конфигурацию по ID"""
    config = db.query(Configuration).options(
        joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.category),
        joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.stock)
    ).filter(Configuration.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    return config


@router.get("/configurations/uuid/{public_uuid}", response_model=ConfigurationResponse)
async def get_configuration_by_uuid(public_uuid: str, db: Session = Depends(get_db)):
    """Получить конфигурацию по публичному UUID"""
    config = db.query(Configuration).options(
        joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.category),
        joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.stock)
    ).filter(Configuration.public_uuid == public_uuid).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    return config


@router.post("/configurations/{config_id}/items")
async def add_component_to_configuration(
    config_id: UUID,
    item_data: ConfigurationItemCreate,
    db: Session = Depends(get_db)
):
    """Добавить компонент в конфигурацию"""
    
    # Проверяем существование конфигурации
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    # Проверяем существование компонента
    component = db.query(Component).filter(Component.id == item_data.component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Компонент не найден")
    
    # Проверяем, нет ли уже такого компонента в конфигурации
    existing_item = db.query(ConfigurationItem).filter(
        ConfigurationItem.configuration_id == config_id,
        ConfigurationItem.component_id == item_data.component_id
    ).first()
    
    if existing_item:
        # Обновляем количество
        existing_item.quantity = item_data.quantity
        existing_item.notes = item_data.notes
        db.commit()
        db.refresh(existing_item)
        
        # Обновляем общую стоимость конфигурации
        await _update_configuration_totals(config_id, db)
        
        return {"message": "Компонент обновлен в конфигурации"}
    else:
        # Создаем новый элемент
        db_item = ConfigurationItem(
            configuration_id=config_id,
            component_id=item_data.component_id,
            quantity=item_data.quantity,
            notes=item_data.notes,
            price_snapshot=component.price
        )
        
        db.add(db_item)
        db.commit()
        
        # Обновляем общую стоимость конфигурации
        await _update_configuration_totals(config_id, db)
        
        return {"message": "Компонент добавлен в конфигурацию"}


@router.delete("/configurations/{config_id}/items/{item_id}")
async def remove_component_from_configuration(
    config_id: UUID,
    item_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить компонент из конфигурации"""
    
    item = db.query(ConfigurationItem).filter(
        ConfigurationItem.id == item_id,
        ConfigurationItem.configuration_id == config_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Элемент конфигурации не найден")
    
    db.delete(item)
    db.commit()
    
    # Обновляем общую стоимость конфигурации
    await _update_configuration_totals(config_id, db)
    
    return {"message": "Компонент удален из конфигурации"}


@router.post("/configurations/{config_id}/check-compatibility", response_model=CompatibilityCheck)
async def check_configuration_compatibility(config_id: UUID, db: Session = Depends(get_db)):
    """Проверить совместимость конфигурации"""
    
    # Получаем все компоненты конфигурации
    config_items = db.query(ConfigurationItem).filter(
        ConfigurationItem.configuration_id == config_id
    ).all()
    
    if not config_items:
        raise HTTPException(status_code=400, detail="Конфигурация пуста")
    
    component_ids = [item.component_id for item in config_items]
    
    compatibility_service = CompatibilityService(db)
    result = compatibility_service.check_configuration_compatibility(component_ids)
    
    # Обновляем статус совместимости в конфигурации
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if config:
        config.compatibility_status = result.status.value
        config.compatibility_issues = [issue.dict() for issue in result.issues]
        db.commit()
    
    return result


@router.get("/configurations/{config_id}/export/pdf")
async def export_configuration_pdf(config_id: UUID, db: Session = Depends(get_db)):
    """Экспортировать конфигурацию в PDF"""
    
    # Получаем конфигурацию
    config = db.query(Configuration).options(
        joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.category),
        joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.stock)
    ).filter(Configuration.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    if not config.items:
        raise HTTPException(status_code=400, detail="Конфигурация пуста")
    
    # Проверяем совместимость
    component_ids = [item.component_id for item in config.items]
    compatibility_service = CompatibilityService(db)
    compatibility_check = compatibility_service.check_configuration_compatibility(component_ids)
    
    # Создаем данные для экспорта
    export_data = ConfigurationExport(
        configuration=config,
        compatibility_check=compatibility_check,
        export_date=datetime.now(),
        notes="Конфигурация создана с помощью веб-конфигуратора ПК"
    )
    
    # Генерируем HTML файл
    pdf_service = PDFService()
    html_path = pdf_service.generate_configuration_pdf(export_data)
    
    # Обновляем статус конфигурации
    config.status = "exported"
    db.commit()
    
    return FileResponse(
        html_path,
        media_type="text/html",
        filename=f"configuration_{config.name}.html"
    )


@router.put("/configurations/{config_id}", response_model=ConfigurationResponse)
async def update_configuration(
    config_id: UUID,
    config_data: ConfigurationCreate,
    db: Session = Depends(get_db)
):
    """Обновить конфигурацию"""
    
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    config.name = config_data.name
    config.description = config_data.description
    config.updated_at = datetime.now()
    
    db.commit()
    db.refresh(config)
    
    return config


@router.delete("/configurations/{config_id}")
async def delete_configuration(config_id: UUID, db: Session = Depends(get_db)):
    """Удалить конфигурацию"""
    
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    db.delete(config)
    db.commit()
    
    return {"message": "Конфигурация удалена"}


async def _update_configuration_totals(config_id: UUID, db: Session):
    """Обновить общие показатели конфигурации"""
    
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not config:
        return
    
    # Получаем все элементы конфигурации
    items = db.query(ConfigurationItem).options(
        joinedload(ConfigurationItem.component).joinedload(Component.stock)
    ).filter(ConfigurationItem.configuration_id == config_id).all()
    
    # Считаем общую стоимость
    total_price = sum(
        (item.price_snapshot or item.component.price) * item.quantity 
        for item in items
    )
    
    # Определяем статус наличия
    availability_statuses = []
    for item in items:
        if item.component.stock:
            availability_statuses.append(item.component.stock.status)
        else:
            availability_statuses.append("out_of_stock")
    
    if all(status == "in_stock" for status in availability_statuses):
        availability_status = "available"
    elif any(status == "in_stock" for status in availability_statuses):
        availability_status = "partial"
    else:
        availability_status = "unavailable"
    
    # Обновляем конфигурацию
    config.total_price = total_price
    config.availability_status = availability_status
    config.updated_at = datetime.now()
    
    db.commit()