from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from ..models import Component
from ..schemas.configuration import CompatibilityCheck, CompatibilityIssue, CompatibilityStatus


class CompatibilityService:
    """Сервис для проверки совместимости компонентов ПК"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_configuration_compatibility(self, component_ids: List[UUID]) -> CompatibilityCheck:
        """Проверка совместимости конфигурации"""
        components = self.db.query(Component).filter(Component.id.in_(component_ids)).all()
        
        if not components:
            return CompatibilityCheck(
                is_compatible=False,
                status=CompatibilityStatus.UNKNOWN,
                issues=[],
                total_power_consumption=None,
                recommended_psu_wattage=None
            )
        
        # Группируем компоненты по категориям
        components_by_category = {}
        for comp in components:
            category_slug = comp.category.slug
            if category_slug not in components_by_category:
                components_by_category[category_slug] = []
            components_by_category[category_slug].append(comp)
        
        issues = []
        total_power = 0
        
        # Проверяем основные совместимости
        issues.extend(self._check_cpu_motherboard_compatibility(components_by_category))
        issues.extend(self._check_ram_motherboard_compatibility(components_by_category))
        issues.extend(self._check_case_motherboard_compatibility(components_by_category))
        
        # Считаем энергопотребление
        total_power = self._calculate_total_power_consumption(components)
        power_issues = self._check_power_supply_compatibility(components_by_category, total_power)
        issues.extend(power_issues)
        
        # Определяем общий статус
        status = self._determine_compatibility_status(issues)
        is_compatible = status == CompatibilityStatus.COMPATIBLE
        
        # Рекомендуемая мощность БП (с запасом 20%)
        recommended_psu = int(total_power * 1.2) if total_power > 0 else None
        
        return CompatibilityCheck(
            is_compatible=is_compatible,
            status=status,
            issues=issues,
            total_power_consumption=total_power,
            recommended_psu_wattage=recommended_psu
        )
    
    def _check_cpu_motherboard_compatibility(self, components_by_category: Dict[str, List[Component]]) -> List[CompatibilityIssue]:
        """Проверка совместимости процессора и материнской платы"""
        issues = []
        
        cpus = components_by_category.get('cpu', [])
        motherboards = components_by_category.get('motherboard', [])
        
        if len(cpus) == 1 and len(motherboards) == 1:
            cpu = cpus[0]
            motherboard = motherboards[0]
            
            cpu_socket = cpu.specifications.get('socket')
            mb_socket = motherboard.specifications.get('socket')
            
            if cpu_socket and mb_socket and cpu_socket != mb_socket:
                issues.append(CompatibilityIssue(
                    type="socket_mismatch",
                    severity="error",
                    message=f"Несовместимые сокеты: процессор {cpu_socket}, материнская плата {mb_socket}",
                    component_ids=[cpu.id, motherboard.id],
                    suggestions=[
                        f"Выберите процессор с сокетом {mb_socket}",
                        f"Выберите материнскую плату с сокетом {cpu_socket}"
                    ]
                ))
        
        return issues
    
    def _check_ram_motherboard_compatibility(self, components_by_category: Dict[str, List[Component]]) -> List[CompatibilityIssue]:
        """Проверка совместимости RAM и материнской платы"""
        issues = []
        
        ram_modules = components_by_category.get('ram', [])
        motherboards = components_by_category.get('motherboard', [])
        
        if ram_modules and len(motherboards) == 1:
            motherboard = motherboards[0]
            mb_memory_type = motherboard.specifications.get('memory_type', [])
            mb_max_memory = motherboard.specifications.get('max_memory_gb', 0)
            mb_memory_slots = motherboard.specifications.get('memory_slots', 0)
            
            total_ram_gb = 0
            for ram in ram_modules:
                ram_type = ram.specifications.get('memory_type')
                ram_capacity = ram.specifications.get('capacity_gb', 0)
                total_ram_gb += ram_capacity
                
                # Проверяем тип памяти
                if ram_type and mb_memory_type and ram_type not in mb_memory_type:
                    issues.append(CompatibilityIssue(
                        type="memory_type_mismatch",
                        severity="error",
                        message=f"Тип памяти {ram_type} не поддерживается материнской платой",
                        component_ids=[ram.id, motherboard.id],
                        suggestions=[f"Выберите память типа {', '.join(mb_memory_type)}"]
                    ))
            
            # Проверяем максимальный объем
            if mb_max_memory > 0 and total_ram_gb > mb_max_memory:
                issues.append(CompatibilityIssue(
                    type="memory_capacity_exceeded",
                    severity="warning",
                    message=f"Объем памяти ({total_ram_gb}ГБ) превышает максимум материнской платы ({mb_max_memory}ГБ)",
                    component_ids=[ram.id for ram in ram_modules] + [motherboard.id],
                    suggestions=[f"Уменьшите объем памяти до {mb_max_memory}ГБ"]
                ))
            
            # Проверяем количество слотов
            if mb_memory_slots > 0 and len(ram_modules) > mb_memory_slots:
                issues.append(CompatibilityIssue(
                    type="memory_slots_exceeded",
                    severity="error",
                    message=f"Количество модулей памяти ({len(ram_modules)}) превышает количество слотов ({mb_memory_slots})",
                    component_ids=[ram.id for ram in ram_modules] + [motherboard.id],
                    suggestions=[f"Используйте не более {mb_memory_slots} модулей памяти"]
                ))
        
        return issues
    
    def _check_case_motherboard_compatibility(self, components_by_category: Dict[str, List[Component]]) -> List[CompatibilityIssue]:
        """Проверка совместимости корпуса и материнской платы"""
        issues = []
        
        cases = components_by_category.get('case', [])
        motherboards = components_by_category.get('motherboard', [])
        
        if len(cases) == 1 and len(motherboards) == 1:
            case = cases[0]
            motherboard = motherboards[0]
            
            case_form_factors = case.specifications.get('supported_form_factors', [])
            mb_form_factor = motherboard.form_factor
            
            if mb_form_factor and case_form_factors and mb_form_factor not in case_form_factors:
                issues.append(CompatibilityIssue(
                    type="form_factor_mismatch",
                    severity="error",
                    message=f"Форм-фактор материнской платы {mb_form_factor} не поддерживается корпусом",
                    component_ids=[case.id, motherboard.id],
                    suggestions=[f"Выберите корпус с поддержкой {mb_form_factor}"]
                ))
        
        return issues
    
    def _check_power_supply_compatibility(self, components_by_category: Dict[str, List[Component]], total_power: int) -> List[CompatibilityIssue]:
        """Проверка совместимости блока питания"""
        issues = []
        
        psus = components_by_category.get('psu', [])
        
        if len(psus) == 1 and total_power > 0:
            psu = psus[0]
            psu_wattage = psu.specifications.get('wattage', 0)
            
            # Рекомендуем запас в 20%
            recommended_wattage = int(total_power * 1.2)
            
            if psu_wattage < total_power:
                issues.append(CompatibilityIssue(
                    type="power_insufficient",
                    severity="error",
                    message=f"Мощность БП ({psu_wattage}Вт) недостаточна для системы ({total_power}Вт)",
                    component_ids=[psu.id],
                    suggestions=[f"Выберите БП мощностью от {recommended_wattage}Вт"]
                ))
            elif psu_wattage < recommended_wattage:
                issues.append(CompatibilityIssue(
                    type="power_warning",
                    severity="warning",
                    message=f"Рекомендуется БП большей мощности для надежности ({recommended_wattage}Вт+)",
                    component_ids=[psu.id],
                    suggestions=[f"Рассмотрите БП мощностью {recommended_wattage}Вт+ для большего запаса"]
                ))
        
        return issues
    
    def _calculate_total_power_consumption(self, components: List[Component]) -> int:
        """Расчет общего энергопотребления"""
        total_power = 0
        
        for component in components:
            if component.power_consumption:
                total_power += component.power_consumption
        
        return total_power
    
    def _determine_compatibility_status(self, issues: List[CompatibilityIssue]) -> CompatibilityStatus:
        """Определение общего статуса совместимости"""
        if not issues:
            return CompatibilityStatus.COMPATIBLE
        
        has_errors = any(issue.severity == "error" for issue in issues)
        has_warnings = any(issue.severity == "warning" for issue in issues)
        
        if has_errors:
            return CompatibilityStatus.INCOMPATIBLE
        elif has_warnings:
            return CompatibilityStatus.WARNING
        else:
            return CompatibilityStatus.COMPATIBLE 