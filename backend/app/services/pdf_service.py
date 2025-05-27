import os
import tempfile
import logging
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from jinja2 import Environment, FileSystemLoader
from ..schemas.configuration import ConfigurationExport
from ..config import settings

# Настройка логирования
logger = logging.getLogger(__name__)

class PDFService:
    """Сервис для генерации PDF отчетов"""
    
    def __init__(self):
        # Настройка Jinja2 для шаблонов
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        
        # Регистрируем русские шрифты
        self._register_fonts()
    
    def _register_fonts(self):
        """Регистрация шрифтов для поддержки русского языка"""
        try:
            # Пытаемся использовать системные шрифты
            font_paths = [
                '/System/Library/Fonts/Arial.ttf',  # macOS
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
                '/Windows/Fonts/arial.ttf',  # Windows
                '/usr/share/fonts/TTF/DejaVuSans.ttf',  # Arch Linux
            ]
            
            font_registered = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                        font_registered = True
                        logger.info(f"Зарегистрирован шрифт: {font_path}")
                        break
                    except Exception as e:
                        logger.warning(f"Не удалось зарегистрировать шрифт {font_path}: {e}")
            
            if not font_registered:
                logger.warning("Не удалось найти подходящий шрифт, будет использован стандартный")
                
        except Exception as e:
            logger.error(f"Ошибка регистрации шрифтов: {e}")
    
    def generate_configuration_pdf(self, export_data: ConfigurationExport) -> str:
        """Генерация PDF отчета конфигурации"""
        
        logger.info(f"Начинаю генерацию PDF для конфигурации {export_data.configuration.id}")
        
        # Создаем временный файл для PDF
        pdf_filename = f"config_{export_data.configuration.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(settings.PDF_TEMP_PATH, pdf_filename)
        
        # Создаем директорию если её нет
        os.makedirs(settings.PDF_TEMP_PATH, exist_ok=True)
        logger.info(f"Создана директория: {settings.PDF_TEMP_PATH}")
        
        try:
            # Генерируем PDF с помощью reportlab
            logger.info("Создаю PDF с помощью reportlab")
            self._generate_modern_pdf(export_data, pdf_path)
            
            # Проверяем, что файл действительно создан
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                logger.info(f"PDF файл создан, размер: {file_size} байт")
                return pdf_path
            else:
                raise Exception("PDF файл не был создан")
            
        except Exception as e:
            # В случае ошибки генерируем HTML отчет с помощью Jinja2 шаблона
            logger.error(f"Ошибка генерации PDF: {e}", exc_info=True)
            
            # Создаем HTML файл с помощью Jinja2 шаблона
            html_filename = f"config_{export_data.configuration.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            html_path = os.path.join(settings.PDF_TEMP_PATH, html_filename)
            
            logger.info("Создаю HTML файл с помощью Jinja2 шаблона")
            html_content = self._generate_html_from_template(export_data)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML файл создан: {html_path}")
            return html_path
    
    def _generate_html_from_template(self, export_data: ConfigurationExport) -> str:
        """Генерация HTML отчета с помощью Jinja2 шаблона"""
        
        config = export_data.configuration
        compatibility = export_data.compatibility_check
        
        # Подготавливаем данные для шаблона
        components_total = sum((item.price_snapshot or item.component.price) * item.quantity for item in config.items)
        accessories_total = sum((acc.price_snapshot or acc.component.price) * acc.quantity for acc in config.accessories) if config.accessories else 0
        total_price = components_total + accessories_total
        
        # Группируем компоненты по категориям
        components_by_category = {}
        for item in config.items:
            category = item.component.category.name
            if category not in components_by_category:
                components_by_category[category] = []
            
            component_data = {
                'brand': item.component.brand,
                'name': item.component.name,
                'model': item.component.model,
                'quantity': item.quantity,
                'price': item.price_snapshot or item.component.price,
                'total': (item.price_snapshot or item.component.price) * item.quantity,
                'stock_status': self._get_stock_status_text(item.component.stock.status if item.component.stock else 'unknown'),
                'specifications': self._format_specifications(item.component.specifications) if item.component.specifications else None
            }
            components_by_category[category].append(component_data)
        
        # Подготавливаем данные аксессуаров
        accessories = []
        if config.accessories:
            for acc in config.accessories:
                accessories.append({
                    'component': acc.component,
                    'quantity': acc.quantity,
                    'price_snapshot': acc.price_snapshot,
                    'notes': acc.notes
                })
        
        # Подготавливаем данные для шаблона
        template_data = {
            'config': config,
            'export_date': export_data.export_date.strftime('%d.%m.%Y %H:%M'),
            'components_total': components_total,
            'accessories_total': accessories_total,
            'total_price': total_price,
            'total_power': compatibility.total_power_consumption,
            'compatibility_status': self._get_compatibility_status_text(compatibility.status),
            'components_by_category': components_by_category,
            'accessories': accessories,
            'compatibility_issues': compatibility.issues,
            'recommended_psu': compatibility.recommended_psu_wattage,
            'notes': export_data.notes
        }
        
        # Рендерим шаблон
        template = self.jinja_env.get_template('configuration_pdf.html')
        return template.render(**template_data)
    
    def _get_compatibility_status_text(self, status: str) -> str:
        """Получить текстовое описание статуса совместимости"""
        status_map = {
            "compatible": "Совместимо",
            "incompatible": "Несовместимо", 
            "warning": "Предупреждения",
            "unknown": "Неизвестно"
        }
        return status_map.get(status.lower(), "Неизвестно")
    
    def _get_stock_status_text(self, status: str) -> str:
        """Преобразовать статус наличия в текст"""
        status_map = {
            "in_stock": "В наличии",
            "expected": "Ожидается",
            "out_of_stock": "Нет в наличии"
        }
        return status_map.get(status, "Неизвестно")
    
    def _get_issue_type_text(self, issue_type: str) -> str:
        """Преобразовать тип проблемы в текст"""
        type_map = {
            "socket_mismatch": "Несовместимость сокетов",
            "memory_type_mismatch": "Несовместимость типа памяти",
            "memory_capacity_exceeded": "Превышение объема памяти",
            "memory_slots_exceeded": "Превышение количества слотов",
            "form_factor_mismatch": "Несовместимость форм-фактора",
            "power_insufficient": "Недостаточная мощность БП",
            "power_warning": "Предупреждение о мощности БП"
        }
        return type_map.get(issue_type, issue_type)
    
    def _get_severity_text(self, severity: str) -> str:
        """Преобразовать серьезность проблемы в текст"""
        severity_map = {
            "error": "Ошибка",
            "warning": "Предупреждение",
            "info": "Информация"
        }
        return severity_map.get(severity, severity)
    
    def _format_specifications(self, specs: dict) -> str:
        """Форматировать технические характеристики"""
        if not specs:
            return ""
        
        formatted = []
        for key, value in specs.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            formatted.append(f"{key}: {value}")
        
        return " | ".join(formatted)

    def _generate_modern_pdf(self, export_data: ConfigurationExport, pdf_path: str):
        """Генерация современного PDF отчета в стиле фронтенда"""
        
        config = export_data.configuration
        compatibility = export_data.compatibility_check
        
        # Создаем документ с отступами
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        story = []
        
        # Определяем шрифт
        font_name = 'DejaVuSans' if 'DejaVuSans' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        
        # Создаем стили в современном минималистичном дизайне
        styles = self._create_modern_styles(font_name)
        
        # === ЗАГОЛОВОК ===
        story.append(Paragraph("КОНФИГУРАЦИЯ ПК", styles['title']))
        story.append(Spacer(1, 0.3*cm))
        
        # Название конфигурации
        story.append(Paragraph(config.name, styles['config_name']))
        if config.description:
            story.append(Spacer(1, 0.2*cm))
            story.append(Paragraph(config.description, styles['description']))
        
        story.append(Spacer(1, 0.5*cm))
        
        # Дата экспорта
        export_date_str = export_data.export_date.strftime('%d.%m.%Y в %H:%M')
        story.append(Paragraph(f"Дата создания отчета: {export_date_str}", styles['meta']))
        
        story.append(Spacer(1, 1*cm))
        
        # === ОБЩАЯ ИНФОРМАЦИЯ ===
        components_total = sum((item.price_snapshot or item.component.price) * item.quantity for item in config.items)
        accessories_total = sum((acc.price_snapshot or acc.component.price) * acc.quantity for acc in config.accessories) if config.accessories else 0
        total_price = components_total + accessories_total
        
        # Создаем таблицу с общей информацией
        info_data = [
            ['СТОИМОСТЬ КОМПОНЕНТОВ', f'{components_total:,.0f} ₽'.replace(',', ' ')],
        ]
        
        if accessories_total > 0:
            info_data.append(['СТОИМОСТЬ АКСЕССУАРОВ', f'{accessories_total:,.0f} ₽'.replace(',', ' ')])
        
        info_data.extend([
            ['ОБЩАЯ СТОИМОСТЬ', f'{total_price:,.0f} ₽'.replace(',', ' ')],
            ['СТАТУС СОВМЕСТИМОСТИ', self._get_compatibility_status_text(compatibility.status)],
        ])
        
        if compatibility.total_power_consumption:
            info_data.append(['ЭНЕРГОПОТРЕБЛЕНИЕ', f'{compatibility.total_power_consumption} Вт'])
        if compatibility.recommended_psu_wattage:
            info_data.append(['РЕКОМЕНДУЕМЫЙ БП', f'{compatibility.recommended_psu_wattage} Вт'])
        
        info_table = Table(info_data, colWidths=[6*cm, 6*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), font_name),  # Жирный для левой колонки
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2563eb')),  # Синяя линия под заголовком
            # Выделяем строку с общей стоимостью
            ('BACKGROUND', (0, -4 if accessories_total > 0 else -3), (-1, -4 if accessories_total > 0 else -3), colors.HexColor('#e0f2fe')),
            ('TEXTCOLOR', (1, -4 if accessories_total > 0 else -3), (1, -4 if accessories_total > 0 else -3), colors.HexColor('#01579b')),
            ('FONTSIZE', (0, -4 if accessories_total > 0 else -3), (-1, -4 if accessories_total > 0 else -3), 13),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 1*cm))
        
        # === КОМПОНЕНТЫ ===
        story.append(Paragraph("КОМПОНЕНТЫ", styles['section_header']))
        story.append(Spacer(1, 0.5*cm))
        
        # Группируем компоненты по категориям
        components_by_category = {}
        for item in config.items:
            category = item.component.category.name
            if category not in components_by_category:
                components_by_category[category] = []
            components_by_category[category].append(item)
        
        for category, items in components_by_category.items():
            # Заголовок категории
            story.append(Paragraph(category.upper(), styles['category_header']))
            story.append(Spacer(1, 0.3*cm))
            
            # Компоненты в категории
            for item in items:
                price = item.price_snapshot or item.component.price
                
                # Создаем таблицу для каждого компонента
                component_data = [
                    [f"{item.component.brand} {item.component.name}", f'{price:,.0f} ₽'.replace(',', ' ')],
                    [f"Модель: {item.component.model}", f"Количество: {item.quantity}"]
                ]
                
                component_table = Table(component_data, colWidths=[10*cm, 4*cm])
                component_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (1, 0), 12),  # Название компонента
                    ('FONTSIZE', (0, 1), (1, 1), 10),  # Детали
                    ('FONTNAME', (0, 0), (0, 0), font_name),  # Жирный для названия
                    ('FONTNAME', (1, 0), (1, 0), font_name),  # Жирный для цены
                    ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1f2937')),
                    ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#059669')),  # Зеленый для цены
                    ('TEXTCOLOR', (0, 1), (1, 1), colors.HexColor('#6b7280')),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                ]))
                
                story.append(component_table)
                story.append(Spacer(1, 0.4*cm))
        
        # === АКСЕССУАРЫ ===
        if config.accessories:
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph("АКСЕССУАРЫ", styles['section_header']))
            story.append(Spacer(1, 0.5*cm))
            
            for accessory in config.accessories:
                price = accessory.price_snapshot or accessory.component.price
                
                # Создаем таблицу для каждого аксессуара
                accessory_data = [
                    [f"{accessory.component.brand} {accessory.component.name}", f'{price:,.0f} ₽'.replace(',', ' ')],
                    [f"Модель: {accessory.component.model}", f"Количество: {accessory.quantity}"]
                ]
                
                accessory_table = Table(accessory_data, colWidths=[10*cm, 4*cm])
                accessory_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (1, 0), 12),  # Название аксессуара
                    ('FONTSIZE', (0, 1), (1, 1), 10),  # Детали
                    ('FONTNAME', (0, 0), (0, 0), font_name),  # Жирный для названия
                    ('FONTNAME', (1, 0), (1, 0), font_name),  # Жирный для цены
                    ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1f2937')),
                    ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#059669')),  # Зеленый для цены
                    ('TEXTCOLOR', (0, 1), (1, 1), colors.HexColor('#6b7280')),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),  # Слегка другой цвет для аксессуаров
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                ]))
                
                story.append(accessory_table)
                story.append(Spacer(1, 0.4*cm))
        
        # === СОВМЕСТИМОСТЬ ===
        if compatibility.issues:
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph("ПРОБЛЕМЫ СОВМЕСТИМОСТИ", styles['section_header']))
            story.append(Spacer(1, 0.5*cm))
            
            for issue in compatibility.issues:
                # Определяем цвет по серьезности
                severity_colors = {
                    'error': colors.HexColor('#dc2626'),
                    'warning': colors.HexColor('#d97706'),
                    'info': colors.HexColor('#2563eb')
                }
                severity_color = severity_colors.get(issue.severity, colors.HexColor('#6b7280'))
                
                issue_text = f"<b>{self._get_issue_type_text(issue.type)}</b><br/>{issue.message}"
                if issue.suggestions:
                    issue_text += f"<br/><i>Рекомендации: {', '.join(issue.suggestions)}</i>"
                
                issue_para = Paragraph(issue_text, styles['issue'])
                
                # Создаем таблицу для выделения проблемы
                issue_table = Table([[issue_para]], colWidths=[14*cm])
                issue_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef2f2')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('BOX', (0, 0), (-1, -1), 2, severity_color),
                ]))
                
                story.append(issue_table)
                story.append(Spacer(1, 0.3*cm))
        
        # === ФУТЕР ===
        story.append(Spacer(1, 1*cm))
        
        # Линия разделитель
        line_table = Table([['']]*1, colWidths=[14*cm])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Информация о системе
        footer_text = "Конфигурация создана с помощью веб-конфигуратора ПК"
        if config.public_uuid:
            footer_text += f"<br/>UUID: {config.public_uuid}"
        
        story.append(Paragraph(footer_text, styles['footer']))
        
        # Генерируем PDF
        doc.build(story)
    
    def _create_modern_styles(self, font_name: str):
        """Создание современных стилей для PDF"""
        styles = {}
        
        # Заголовок документа
        styles['title'] = ParagraphStyle(
            'Title',
            fontName=font_name,
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Название конфигурации
        styles['config_name'] = ParagraphStyle(
            'ConfigName',
            fontName=font_name,
            fontSize=18,
            textColor=colors.HexColor('#2563eb'),
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Описание
        styles['description'] = ParagraphStyle(
            'Description',
            fontName=font_name,
            fontSize=12,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Метаинформация
        styles['meta'] = ParagraphStyle(
            'Meta',
            fontName=font_name,
            fontSize=10,
            textColor=colors.HexColor('#9ca3af'),
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Заголовки разделов
        styles['section_header'] = ParagraphStyle(
            'SectionHeader',
            fontName=font_name,
            fontSize=16,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Заголовки категорий
        styles['category_header'] = ParagraphStyle(
            'CategoryHeader',
            fontName=font_name,
            fontSize=13,
            textColor=colors.HexColor('#374151'),
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Проблемы совместимости
        styles['issue'] = ParagraphStyle(
            'Issue',
            fontName=font_name,
            fontSize=11,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Футер
        styles['footer'] = ParagraphStyle(
            'Footer',
            fontName=font_name,
            fontSize=9,
            textColor=colors.HexColor('#9ca3af'),
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0,
        )
        
        return styles 