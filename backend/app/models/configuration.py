from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base


class Configuration(Base):
    """Сохраненные конфигурации ПК"""
    __tablename__ = "configurations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    
    # Публичный UUID для общего доступа
    public_uuid = Column(String(36), unique=True, index=True)
    
    # Общая стоимость
    total_price = Column(Numeric(precision=10, scale=2), default=0.0)
    
    # Общее энергопотребление
    total_power_consumption = Column(Integer)
    
    # Проверка совместимости
    compatibility_status = Column(String(20), default="unknown")  # "compatible", "incompatible", "warning"
    compatibility_notes = Column(Text)  # Заметки о совместимости
    compatibility_issues = Column(JSONB)  # JSON структура для хранения проблем совместимости
    
    # Статус наличия
    availability_status = Column(String(20), default="unknown")  # "available", "partial", "unavailable"
    
    # Статус конфигурации
    status = Column(String(20), default="draft")  # "draft", "completed", "exported"
    
    # Публичный доступ
    is_public = Column(Boolean, default=False)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    items = relationship("ConfigurationItem", back_populates="configuration")
    accessories = relationship("ConfigurationAccessory", back_populates="configuration")


class ConfigurationItem(Base):
    """Элементы конфигурации (выбранные компоненты)"""
    __tablename__ = "configuration_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    configuration_id = Column(UUID(as_uuid=True), ForeignKey("configurations.id"), nullable=False, index=True)
    component_id = Column(UUID(as_uuid=True), ForeignKey("components.id"), nullable=False, index=True)
    
    # Количество
    quantity = Column(Integer, default=1)
    
    # Снимок цены на момент добавления
    price_snapshot = Column(Numeric(precision=10, scale=2))
    
    # Дополнительные настройки/комментарии
    notes = Column(Text)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    configuration = relationship("Configuration", back_populates="items")
    component = relationship("Component")


class ConfigurationAccessory(Base):
    """Аксессуары в конфигурации"""
    __tablename__ = "configuration_accessories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    configuration_id = Column(UUID(as_uuid=True), ForeignKey("configurations.id"), nullable=False, index=True)
    component_id = Column(UUID(as_uuid=True), ForeignKey("components.id"), nullable=False, index=True)
    
    # Количество
    quantity = Column(Integer, default=1)
    
    # Снимок цены на момент добавления
    price_snapshot = Column(Numeric(precision=10, scale=2))
    
    # Дополнительные настройки/комментарии
    notes = Column(Text)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    configuration = relationship("Configuration", back_populates="accessories")
    component = relationship("Component") 