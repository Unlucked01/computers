from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from uuid import UUID
from .component import ComponentResponse


class ConfigurationStatus(str, Enum):
    DRAFT = "draft"
    COMPLETED = "completed"
    EXPORTED = "exported"


class CompatibilityStatus(str, Enum):
    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"
    WARNING = "warning"
    UNKNOWN = "unknown"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class ConfigurationCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None


class ConfigurationItemCreate(BaseModel):
    component_id: UUID
    quantity: int = Field(1, ge=1)
    notes: Optional[str] = None


class ConfigurationItemResponse(BaseModel):
    id: UUID
    component: ComponentResponse
    quantity: int
    price_snapshot: Optional[float]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConfigurationResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    public_uuid: Optional[str]
    total_price: float
    total_power_consumption: Optional[int]
    compatibility_status: CompatibilityStatus
    compatibility_notes: Optional[str]
    status: ConfigurationStatus
    is_public: bool
    created_at: datetime
    updated_at: datetime
    items: List[ConfigurationItemResponse]
    
    class Config:
        from_attributes = True


class CompatibilityIssue(BaseModel):
    """Проблема совместимости"""
    type: str  # "socket_mismatch", "power_insufficient", "form_factor_conflict"
    severity: str  # "error", "warning", "info"
    message: str
    component_ids: List[UUID]
    suggestions: Optional[List[str]] = None


class CompatibilityCheck(BaseModel):
    """Результат проверки совместимости"""
    is_compatible: bool
    status: CompatibilityStatus
    issues: List[CompatibilityIssue]
    total_power_consumption: Optional[int]
    recommended_psu_wattage: Optional[int]


class ConfigurationExport(BaseModel):
    """Данные для экспорта конфигурации в PDF"""
    configuration: ConfigurationResponse
    compatibility_check: CompatibilityCheck
    export_date: datetime
    notes: Optional[str] = None 