from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base


class ComponentCategory(Base):
    """Категории компонентов ПК"""
    __tablename__ = "component_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, index=True)  # "Процессоры", "Материнские платы" и т.д.
    slug = Column(String(50), unique=True, nullable=False)   # "cpu", "motherboard" и т.д.
    description = Column(Text)
    order_priority = Column(Integer, default=0)  # Порядок отображения
    icon = Column(String(50))  # CSS класс или имя иконки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    components = relationship("Component", back_populates="category")


class Component(Base):
    """Компоненты ПК"""
    __tablename__ = "components"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, index=True)
    brand = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Цена и наличие
    price = Column(Numeric(precision=10, scale=2), nullable=False, index=True)
    
    # Категория
    category_id = Column(UUID(as_uuid=True), ForeignKey("component_categories.id"), nullable=False, index=True)
    category = relationship("ComponentCategory", back_populates="components")
    
    # Технические характеристики (JSONB для PostgreSQL)
    specifications = Column(JSONB)  # {"socket": "AM4", "cores": 8, "frequency": 3.8, ...}
    
    # Форм-фактор
    form_factor = Column(String(50))  # ATX, mATX, ITX для корпусов/плат
    
    # Энергопотребление
    power_consumption = Column(Integer)  # Ватт
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Связи
    stock = relationship("ComponentStock", back_populates="component", uselist=False)
    compatibility_as_component1 = relationship(
        "ComponentCompatibility", 
        foreign_keys="ComponentCompatibility.component1_id",
        back_populates="component1"
    )
    compatibility_as_component2 = relationship(
        "ComponentCompatibility",
        foreign_keys="ComponentCompatibility.component2_id", 
        back_populates="component2"
    )


class ComponentStock(Base):
    """Наличие компонентов"""
    __tablename__ = "component_stock"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    component_id = Column(UUID(as_uuid=True), ForeignKey("components.id"), nullable=False, index=True)
    
    # Статус наличия
    status = Column(String(20), nullable=False)  # "in_stock", "expected", "out_of_stock"
    quantity = Column(Integer, default=0)
    expected_date = Column(Date)  # Дата поступления
    
    # Метаданные
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    component = relationship("Component", back_populates="stock")


class ComponentCompatibility(Base):
    """Совместимость между компонентами"""
    __tablename__ = "component_compatibility"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    component1_id = Column(UUID(as_uuid=True), ForeignKey("components.id"), nullable=False, index=True)
    component2_id = Column(UUID(as_uuid=True), ForeignKey("components.id"), nullable=False, index=True)
    
    # Тип совместимости
    compatibility_type = Column(String(20), nullable=False)  # "compatible", "incompatible", "warning"
    
    # Дополнительная информация
    notes = Column(Text)  # Комментарии о совместимости
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    component1 = relationship("Component", foreign_keys=[component1_id])
    component2 = relationship("Component", foreign_keys=[component2_id]) 