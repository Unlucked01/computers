from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from ..models import Component, ComponentCategory, ComponentStock
from ..schemas.component import ComponentCreate, ComponentFilter


class ComponentService:
    """Сервис для работы с компонентами"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_components_with_filters(self, filters: ComponentFilter) -> List[Component]:
        """Получить компоненты с применением фильтров"""
        
        query = self.db.query(Component).options(
            joinedload(Component.category),
            joinedload(Component.stock)
        ).filter(Component.is_active == True)
        
        # Применяем фильтры
        query = self._apply_filters(query, filters)
        
        # Пагинация
        offset = (filters.page - 1) * filters.limit
        components = query.offset(offset).limit(filters.limit).all()
        
        return components
    
    def get_compatible_components(
        self, 
        category_slug: str, 
        compatible_with_ids: List[int]
    ) -> List[Component]:
        """Получить компоненты категории, совместимые с указанными"""
        
        # Получаем категорию
        category = self.db.query(ComponentCategory).filter(
            ComponentCategory.slug == category_slug
        ).first()
        
        if not category:
            return []
        
        # Получаем все компоненты категории
        components = self.db.query(Component).options(
            joinedload(Component.category),
            joinedload(Component.stock)
        ).filter(
            Component.category_id == category.id,
            Component.is_active == True
        ).all()
        
        # Если нет базовых компонентов для проверки, возвращаем все
        if not compatible_with_ids:
            return components
        
        # Фильтруем по совместимости
        compatible_components = []
        existing_components = self._get_components_by_ids(compatible_with_ids)
        
        for component in components:
            if self._is_component_compatible(component, existing_components):
                compatible_components.append(component)
        
        return compatible_components
    
    def get_filter_options(self, category_slug: Optional[str] = None) -> Dict[str, Any]:
        """Получить доступные варианты для фильтров"""
        
        query = self.db.query(Component).filter(Component.is_active == True)
        
        if category_slug:
            query = query.join(ComponentCategory).filter(
                ComponentCategory.slug == category_slug
            )
        
        components = query.all()
        
        return self._extract_filter_options(components)
    
    def _apply_filters(self, query, filters: ComponentFilter):
        """Применить фильтры к запросу"""
        
        # Фильтр по категории
        if filters.category_slug:
            query = query.join(ComponentCategory).filter(
                ComponentCategory.slug == filters.category_slug
            )
        
        # Фильтр по бренду
        if filters.brand:
            query = query.filter(Component.brand.in_(filters.brand))
        
        # Фильтр по цене
        if filters.price_min is not None:
            query = query.filter(Component.price >= filters.price_min)
        if filters.price_max is not None:
            query = query.filter(Component.price <= filters.price_max)
        
        # Фильтр по наличию
        if filters.only_in_stock:
            query = query.join(ComponentStock).filter(
                ComponentStock.status == "in_stock"
            )
        
        # Фильтр по форм-фактору
        if filters.form_factor:
            query = query.filter(Component.form_factor.in_(filters.form_factor))
        
        # Фильтр по энергопотреблению
        if filters.power_max is not None:
            query = query.filter(
                or_(
                    Component.power_consumption <= filters.power_max,
                    Component.power_consumption.is_(None)
                )
            )
        
        # Поиск по тексту
        if filters.search:
            search_filter = or_(
                Component.name.ilike(f"%{filters.search}%"),
                Component.model.ilike(f"%{filters.search}%"),
                Component.brand.ilike(f"%{filters.search}%")
            )
            query = query.filter(search_filter)
        
        # Специфичные фильтры
        if filters.socket:
            query = query.filter(
                Component.specifications["socket"].astext.in_(filters.socket)
            )
        
        if filters.memory_type:
            query = query.filter(
                Component.specifications["memory_type"].astext.in_(filters.memory_type)
            )
        
        if filters.interface:
            query = query.filter(
                Component.specifications["interface"].astext.in_(filters.interface)
            )
        
        return query
    
    def _get_components_by_ids(self, component_ids: List[int]) -> List[Component]:
        """Получить компоненты по ID"""
        return self.db.query(Component).filter(
            Component.id.in_(component_ids)
        ).all()
    
    def _is_component_compatible(
        self, 
        component: Component, 
        existing_components: List[Component]
    ) -> bool:
        """Проверить совместимость компонента с существующими"""
        
        # Простая проверка совместимости по основным параметрам
        for existing in existing_components:
            if not self._check_basic_compatibility(component, existing):
                return False
        
        return True
    
    def _check_basic_compatibility(
        self, 
        component1: Component, 
        component2: Component
    ) -> bool:
        """Базовая проверка совместимости между двумя компонентами"""
        
        # Процессор + Материнская плата: проверка сокета
        if (component1.category.slug == "cpu" and component2.category.slug == "motherboard") or \
           (component1.category.slug == "motherboard" and component2.category.slug == "cpu"):
            
            socket1 = component1.specifications.get("socket")
            socket2 = component2.specifications.get("socket")
            
            if socket1 and socket2 and socket1 != socket2:
                return False
        
        # RAM + Материнская плата: проверка типа памяти
        if (component1.category.slug == "ram" and component2.category.slug == "motherboard") or \
           (component1.category.slug == "motherboard" and component2.category.slug == "ram"):
            
            ram_type = None
            mb_supported_types = None
            
            if component1.category.slug == "ram":
                ram_type = component1.specifications.get("memory_type")
                mb_supported_types = component2.specifications.get("memory_type", [])
            else:
                ram_type = component2.specifications.get("memory_type") 
                mb_supported_types = component1.specifications.get("memory_type", [])
            
            if ram_type and mb_supported_types:
                if isinstance(mb_supported_types, str):
                    mb_supported_types = [mb_supported_types]
                if ram_type not in mb_supported_types:
                    return False
        
        # Корпус + Материнская плата: проверка форм-фактора
        if (component1.category.slug == "case" and component2.category.slug == "motherboard") or \
           (component1.category.slug == "motherboard" and component2.category.slug == "case"):
            
            case_supported = None
            mb_form_factor = None
            
            if component1.category.slug == "case":
                case_supported = component1.specifications.get("supported_form_factors", [])
                mb_form_factor = component2.form_factor
            else:
                case_supported = component2.specifications.get("supported_form_factors", [])
                mb_form_factor = component1.form_factor
            
            if case_supported and mb_form_factor and mb_form_factor not in case_supported:
                return False
        
        return True
    
    def _extract_filter_options(self, components: List[Component]) -> Dict[str, Any]:
        """Извлечь варианты для фильтров из списка компонентов"""
        
        brands = set()
        form_factors = set()
        sockets = set()
        memory_types = set()
        interfaces = set()
        prices = []
        
        for comp in components:
            if comp.brand:
                brands.add(comp.brand)
            
            if comp.form_factor:
                form_factors.add(comp.form_factor)
            
            prices.append(comp.price)
            
            # Извлекаем из specifications
            specs = comp.specifications or {}
            
            if "socket" in specs:
                sockets.add(specs["socket"])
            
            if "memory_type" in specs:
                mem_type = specs["memory_type"]
                if isinstance(mem_type, list):
                    memory_types.update(mem_type)
                else:
                    memory_types.add(mem_type)
            
            if "interface" in specs:
                interfaces.add(specs["interface"])
        
        return {
            "brands": sorted(list(brands)),
            "form_factors": sorted(list(form_factors)),
            "sockets": sorted(list(sockets)),
            "memory_types": sorted(list(memory_types)),
            "interfaces": sorted(list(interfaces)),
            "price_range": {
                "min": min(prices) if prices else 0,
                "max": max(prices) if prices else 0
            }
        } 