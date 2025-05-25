from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from enum import Enum
from uuid import UUID


class StockStatus(str, Enum):
    IN_STOCK = "in_stock"
    EXPECTED = "expected" 
    OUT_OF_STOCK = "out_of_stock"


class ComponentCategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=50)
    description: Optional[str] = None
    order_priority: int = 0
    icon: Optional[str] = None


class ComponentCategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    order_priority: int
    icon: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ComponentStockResponse(BaseModel):
    status: StockStatus
    quantity: int
    expected_date: Optional[date]
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ComponentCreate(BaseModel):
    name: str = Field(..., max_length=200)
    brand: str = Field(..., max_length=100)
    model: str = Field(..., max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: UUID
    specifications: Dict[str, Any] = {}
    form_factor: Optional[str] = None
    power_consumption: Optional[int] = None


class ComponentResponse(BaseModel):
    id: UUID
    name: str
    brand: str
    model: str
    description: Optional[str]
    price: float
    category: ComponentCategoryResponse
    specifications: Dict[str, Any]
    form_factor: Optional[str]
    power_consumption: Optional[int]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    stock: Optional[ComponentStockResponse]
    
    class Config:
        from_attributes = True


class ComponentFilter(BaseModel):
    """Фильтры для поиска компонентов"""
    category_slug: Optional[str] = None
    brand: Optional[List[str]] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    only_in_stock: bool = False
    form_factor: Optional[List[str]] = None
    power_max: Optional[int] = None
    search: Optional[str] = None
    
    # Специфичные фильтры для категорий
    socket: Optional[List[str]] = None  # Для процессоров/материнок
    memory_type: Optional[List[str]] = None  # Для RAM
    interface: Optional[List[str]] = None  # Для накопителей
    
    # Пагинация
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100) 