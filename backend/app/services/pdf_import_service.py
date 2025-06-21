import re
import pdfplumber
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from ..models import Component, ComponentCategory
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


class PDFImportService:
    def __init__(self, db: Session):
        self.db = db
        
    async def import_configuration_from_pdf(self, pdf_content: bytes) -> Dict[str, Any]:
        """
        Импортирует конфигурацию из PDF файла
        """
        try:
            # Извлекаем текст из PDF
            text = self._extract_text_from_pdf(pdf_content)
            
            # Парсим конфигурацию
            config_data = self._parse_configuration_text(text)
            
            # Находим компоненты в базе данных
            components = await self._find_components_in_db(config_data['components'])
            
            return {
                'name': config_data.get('name', 'Импортированная конфигурация'),
                'description': config_data.get('description'),
                'components': components,
                'total_price': float(sum(comp['price'] for comp in components)),
                'compatibility_status': config_data.get('compatibility_status', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Ошибка импорта PDF: {str(e)}")
            raise Exception(f"Не удалось импортировать конфигурацию: {str(e)}")
    
    def _extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Извлекает текст из PDF файла
        """
        text = ""
        try:
            logger.info(f"Начинаю извлечение текста из PDF, размер файла: {len(pdf_content)} байт")
            # Оборачиваем байты в BytesIO для pdfplumber
            pdf_stream = BytesIO(pdf_content)
            with pdfplumber.open(pdf_stream) as pdf:
                logger.info(f"PDF открыт, количество страниц: {len(pdf.pages)}")
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        logger.debug(f"Извлечен текст со страницы {i+1}, длина: {len(page_text)} символов")
                    else:
                        logger.warning(f"Страница {i+1} не содержит текста")
            
            logger.info(f"Извлечение завершено, общая длина текста: {len(text)} символов")
        except Exception as e:
            logger.error(f"Ошибка извлечения текста из PDF: {str(e)}", exc_info=True)
            raise Exception("Не удалось прочитать PDF файл")
        
        return text
    
    def _parse_configuration_text(self, text: str) -> Dict[str, Any]:
        """
        Парсит текст конфигурации и извлекает информацию о компонентах
        """
        logger.info(f"Парсинг PDF текста, длина: {len(text)} символов")
        logger.debug(f"Первые 500 символов текста: {text[:500]}")
        
        config_data = {
            'name': None,
            'description': None,
            'components': [],
            'compatibility_status': 'unknown'
        }
        
        lines = text.split('\n')
        current_category = None
        
        # Паттерны для извлечения информации (более гибкие)
        name_patterns = [
            r'Конфигурация:\s*(.+)',
            r'Название:\s*(.+)',
            r'^(.+?)(?:\s*-\s*Конфигурация)?$'  # Первая строка как название
        ]
        
        # Паттерны категорий (как на русском, так и на английском)
        category_patterns = {
            'Процессоры': 'cpu',
            'Процессор': 'cpu',
            'CPU': 'cpu',
            'Материнские платы': 'motherboard',
            'Материнская плата': 'motherboard', 
            'Motherboard': 'motherboard',
            'Оперативная память': 'ram',
            'RAM': 'ram',
            'Memory': 'ram',
            'Видеокарты': 'gpu',
            'Видеокарта': 'gpu',
            'GPU': 'gpu',
            'Graphics': 'gpu',
            'Накопители': 'storage',
            'Накопитель': 'storage',
            'Storage': 'storage',
            'SSD': 'storage',
            'HDD': 'storage',
            'Блоки питания': 'psu',
            'Блок питания': 'psu',
            'PSU': 'psu',
            'Power Supply': 'psu',
            'Корпуса': 'case',
            'Корпус': 'case',
            'Case': 'case',
            'Охлаждение': 'cooler',
            'Cooler': 'cooler',
            'Cooling': 'cooler'
        }
        
        # Извлекаем название конфигурации
        for i, line in enumerate(lines[:10]):  # Ищем в первых 10 строках
            line = line.strip()
            if line and not any(keyword in line.lower() for keyword in ['pdf', 'page', 'дата', 'date']):
                for pattern in name_patterns:
                    match = re.search(pattern, line)
                    if match:
                        config_data['name'] = match.group(1).strip()
                        break
                if config_data['name']:
                    break
                elif i < 5 and len(line) > 5:  # Если не нашли по паттернам, берем первую содержательную строку
                    config_data['name'] = line
                    break
        
        # Извлекаем статус совместимости
        text_lower = text.lower()
        if 'совместимо' in text_lower or 'compatible' in text_lower:
            config_data['compatibility_status'] = 'compatible'
        elif 'предупреждение' in text_lower or 'warning' in text_lower:
            config_data['compatibility_status'] = 'warning'
        elif 'несовместимо' in text_lower or 'incompatible' in text_lower:
            config_data['compatibility_status'] = 'incompatible'
        
        # Парсим компоненты
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Проверяем, является ли строка категорией
            for category_name, category_slug in category_patterns.items():
                if category_name.lower() in line.lower():
                    current_category = category_slug
                    logger.debug(f"Найдена категория: {category_name} -> {category_slug}")
                    break
            
            # Если у нас есть текущая категория, пытаемся найти компонент
            if current_category:
                # Пропускаем служебные строки
                skip_keywords = ['количество', 'модель', 'наличие', 'характеристики', 'итого', 'всего', 'цена', 'стоимость']
                if any(keyword in line.lower() for keyword in skip_keywords):
                    continue
                
                # Более точные паттерны для компонентов
                component_patterns = [
                    # Паттерн: "Бренд Название ₽12,345" или "Бренд Название 12,345 ₽"
                    r'^([A-Za-z0-9\.\-]+)\s+(.+?)\s+₽?([\d\s,]+)₽?\s*$',
                    # Паттерн: "Полное название ₽12,345"
                    r'^(.+?)\s+₽([\d\s,]+)₽?\s*$'
                ]
                
                for pattern_idx, pattern in enumerate(component_patterns):
                    component_match = re.search(pattern, line.strip())
                    if component_match:
                        if pattern_idx == 0 and len(component_match.groups()) == 3:
                            # Первый паттерн: бренд + название + цена
                            brand = component_match.group(1).strip()
                            name = component_match.group(2).strip()
                            price_str = component_match.group(3).replace(',', '').replace(' ', '')
                        else:
                            # Второй паттерн: полное название + цена
                            full_name = component_match.group(1).strip()
                            price_str = component_match.group(2).replace(',', '').replace(' ', '')
                            
                            # Пытаемся разделить на бренд и название
                            name_parts = full_name.split(' ', 1)
                            if len(name_parts) >= 2:
                                brand = name_parts[0]
                                name = name_parts[1]
                            else:
                                brand = "Unknown"
                                name = full_name
                        
                        try:
                            price = float(price_str)
                            # Проверяем, что цена разумная (больше 100 рублей)
                            if price >= 100:
                                # Проверяем, что такой компонент еще не добавлен
                                already_exists = any(
                                    comp['category'] == current_category and 
                                    comp['brand'].lower() == brand.lower() and 
                                    comp['name'].lower() == name.lower()
                                    for comp in config_data['components']
                                )
                                
                                if not already_exists:
                                    config_data['components'].append({
                                        'category': current_category,
                                        'brand': brand,
                                        'name': name,
                                        'price': price
                                    })
                                    logger.debug(f"Найден компонент: {brand} {name} - {price}₽")
                                    break
                        except ValueError:
                            continue
        
        logger.info(f"Найдено компонентов: {len(config_data['components'])}")
        return config_data
    
    async def _find_components_in_db(self, parsed_components: List[Dict]) -> List[Dict]:
        """
        Находит компоненты в базе данных по названию и бренду
        """
        found_components = []
        
        for comp_data in parsed_components:
            # Ищем компонент в базе данных
            category = self.db.query(ComponentCategory).filter(
                ComponentCategory.slug == comp_data['category']
            ).first()
            
            if not category:
                continue
            
            # Ищем компонент по бренду и названию (нечеткий поиск)
            components = self.db.query(Component).filter(
                Component.category_id == category.id,
                Component.is_active == True,
                Component.brand.ilike(f"%{comp_data['brand']}%")
            ).all()
            
            # Ищем наиболее подходящий компонент
            best_match = None
            best_score = 0
            
            for component in components:
                score = self._calculate_similarity(
                    comp_data['name'].lower(),
                    component.name.lower()
                )
                if score > best_score and score > 0.5:  # Минимальный порог схожести
                    best_match = component
                    best_score = score
            
            if best_match:
                found_components.append({
                    'id': str(best_match.id),
                    'category': comp_data['category'],
                    'name': best_match.name,
                    'brand': best_match.brand,
                    'price': float(best_match.price)
                })
            else:
                # Если не нашли точное соответствие, создаем запись без ID
                # (будет показана как "не найдена в базе")
                found_components.append({
                    'id': None,
                    'category': comp_data['category'],
                    'name': comp_data['name'],
                    'brand': comp_data['brand'],
                    'price': comp_data['price'],
                    'not_found': True
                })
        
        return found_components
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Вычисляет схожесть двух строк (простой алгоритм)
        """
        # Удаляем лишние пробелы и приводим к нижнему регистру
        str1 = ' '.join(str1.split())
        str2 = ' '.join(str2.split())
        
        # Простой алгоритм на основе общих слов
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0