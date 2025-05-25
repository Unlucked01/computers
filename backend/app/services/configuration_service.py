from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import uuid
from ..models import Configuration, ConfigurationItem, Component, ComponentStock
from ..schemas.configuration import ConfigurationCreate, AvailabilityStatus
from .compatibility_service import CompatibilityService


class ConfigurationService:
    """Сервис для работы с конфигурациями ПК"""
    
    def __init__(self, db: Session):
        self.db = db
        self.compatibility_service = CompatibilityService(db)
    
    def create_configuration(self, config_data: ConfigurationCreate) -> Configuration:
        """Создать новую конфигурацию"""
        
        db_config = Configuration(
            name=config_data.name,
            description=config_data.description,
            public_uuid=str(uuid.uuid4())
        )
        
        self.db.add(db_config)
        self.db.commit()
        self.db.refresh(db_config)
        
        return db_config
    
    def add_component_to_configuration(
        self, 
        config_id: int, 
        component_id: int, 
        quantity: int = 1,
        notes: Optional[str] = None
    ) -> ConfigurationItem:
        """Добавить компонент в конфигурацию"""
        
        # Проверяем существование конфигурации и компонента
        config = self.db.query(Configuration).filter(Configuration.id == config_id).first()
        if not config:
            raise ValueError("Конфигурация не найдена")
        
        component = self.db.query(Component).filter(Component.id == component_id).first()
        if not component:
            raise ValueError("Компонент не найден")
        
        # Проверяем, нет ли уже такого компонента
        existing_item = self.db.query(ConfigurationItem).filter(
            ConfigurationItem.configuration_id == config_id,
            ConfigurationItem.component_id == component_id
        ).first()
        
        if existing_item:
            # Обновляем существующий
            existing_item.quantity = quantity
            existing_item.notes = notes
            self.db.commit()
            self.db.refresh(existing_item)
            
            # Обновляем общие показатели
            self._update_configuration_totals(config_id)
            
            return existing_item
        else:
            # Создаем новый
            db_item = ConfigurationItem(
                configuration_id=config_id,
                component_id=component_id,
                quantity=quantity,
                notes=notes,
                price_snapshot=component.price
            )
            
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            
            # Обновляем общие показатели
            self._update_configuration_totals(config_id)
            
            return db_item
    
    def remove_component_from_configuration(self, config_id: int, component_id: int) -> bool:
        """Удалить компонент из конфигурации"""
        
        item = self.db.query(ConfigurationItem).filter(
            ConfigurationItem.configuration_id == config_id,
            ConfigurationItem.component_id == component_id
        ).first()
        
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        
        # Обновляем общие показатели
        self._update_configuration_totals(config_id)
        
        return True
    
    def update_configuration_compatibility(self, config_id: int) -> None:
        """Обновить статус совместимости конфигурации"""
        
        config = self.db.query(Configuration).filter(Configuration.id == config_id).first()
        if not config:
            return
        
        # Получаем все компоненты конфигурации
        items = self.db.query(ConfigurationItem).filter(
            ConfigurationItem.configuration_id == config_id
        ).all()
        
        if not items:
            config.compatibility_status = "unknown"
            config.compatibility_issues = []
            self.db.commit()
            return
        
        # Проверяем совместимость
        component_ids = [item.component_id for item in items]
        compatibility_result = self.compatibility_service.check_configuration_compatibility(component_ids)
        
        # Обновляем конфигурацию
        config.compatibility_status = compatibility_result.status.value
        config.compatibility_issues = [issue.dict() for issue in compatibility_result.issues]
        config.updated_at = datetime.now()
        
        self.db.commit()
    
    def get_configuration_summary(self, config_id: int) -> dict:
        """Получить сводку по конфигурации"""
        
        config = self.db.query(Configuration).options(
            joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.category),
            joinedload(Configuration.items).joinedload(ConfigurationItem.component).joinedload(Component.stock)
        ).filter(Configuration.id == config_id).first()
        
        if not config:
            return {}
        
        # Группируем компоненты по категориям
        components_by_category = {}
        total_power = 0
        total_price = 0
        
        for item in config.items:
            category = item.component.category.name
            if category not in components_by_category:
                components_by_category[category] = []
            
            components_by_category[category].append({
                "component": item.component,
                "quantity": item.quantity,
                "price": item.price_snapshot or item.component.price
            })
            
            # Считаем общее энергопотребление
            if item.component.power_consumption:
                total_power += item.component.power_consumption * item.quantity
            
            # Считаем общую стоимость
            price = item.price_snapshot or item.component.price
            total_price += price * item.quantity
        
        # Проверяем совместимость
        component_ids = [item.component_id for item in config.items]
        compatibility = self.compatibility_service.check_configuration_compatibility(component_ids)
        
        return {
            "configuration": config,
            "components_by_category": components_by_category,
            "total_power_consumption": total_power,
            "total_price": total_price,
            "compatibility": compatibility,
            "missing_categories": self._get_missing_categories(config.items)
        }
    
    def _update_configuration_totals(self, config_id: int) -> None:
        """Обновить общие показатели конфигурации"""
        
        config = self.db.query(Configuration).filter(Configuration.id == config_id).first()
        if not config:
            return
        
        # Получаем все элементы конфигурации с компонентами
        items = self.db.query(ConfigurationItem).options(
            joinedload(ConfigurationItem.component).joinedload(Component.stock)
        ).filter(ConfigurationItem.configuration_id == config_id).all()
        
        if not items:
            config.total_price = 0.0
            config.availability_status = AvailabilityStatus.UNKNOWN.value
            config.expected_delivery_date = None
            self.db.commit()
            return
        
        # Считаем общую стоимость
        total_price = 0.0
        for item in items:
            price = item.price_snapshot or item.component.price
            total_price += price * item.quantity
        
        # Определяем статус наличия
        availability_status = self._calculate_availability_status(items)
        
        # Определяем ожидаемую дату поставки
        expected_date = self._calculate_expected_delivery_date(items)
        
        # Обновляем конфигурацию
        config.total_price = total_price
        config.availability_status = availability_status.value
        config.expected_delivery_date = expected_date
        config.updated_at = datetime.now()
        
        self.db.commit()
        
        # Обновляем совместимость
        self.update_configuration_compatibility(config_id)
    
    def _calculate_availability_status(self, items: List[ConfigurationItem]) -> AvailabilityStatus:
        """Рассчитать статус наличия конфигурации"""
        
        stock_statuses = []
        for item in items:
            if item.component.stock:
                stock_statuses.append(item.component.stock.status)
            else:
                stock_statuses.append("out_of_stock")
        
        if all(status == "in_stock" for status in stock_statuses):
            return AvailabilityStatus.AVAILABLE
        elif any(status == "in_stock" for status in stock_statuses):
            return AvailabilityStatus.PARTIAL
        elif any(status == "expected" for status in stock_statuses):
            return AvailabilityStatus.PARTIAL
        else:
            return AvailabilityStatus.UNAVAILABLE
    
    def _calculate_expected_delivery_date(self, items: List[ConfigurationItem]) -> Optional[datetime]:
        """Рассчитать ожидаемую дату поставки"""
        
        expected_dates = []
        for item in items:
            if item.component.stock and item.component.stock.expected_date:
                expected_dates.append(item.component.stock.expected_date)
        
        if expected_dates:
            # Возвращаем самую позднюю дату
            return max(expected_dates)
        
        return None
    
    def _get_missing_categories(self, items: List[ConfigurationItem]) -> List[str]:
        """Получить список отсутствующих категорий"""
        
        # Основные категории для полной сборки ПК
        essential_categories = [
            "cpu", "motherboard", "ram", "storage", 
            "gpu", "psu", "case"
        ]
        
        # Получаем категории, которые уже есть в конфигурации
        existing_categories = set()
        for item in items:
            existing_categories.add(item.component.category.slug)
        
        # Находим недостающие
        missing = []
        for category in essential_categories:
            if category not in existing_categories:
                # Получаем человекочитаемое название категории
                cat_obj = self.db.query(ComponentCategory).filter(
                    ComponentCategory.slug == category
                ).first()
                if cat_obj:
                    missing.append(cat_obj.name)
        
        return missing 