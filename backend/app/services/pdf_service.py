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
            # В случае ошибки генерируем простой HTML отчет как fallback
            logger.error(f"Ошибка генерации PDF: {e}", exc_info=True)
            
            # Создаем HTML файл как резервный вариант
            html_filename = f"config_{export_data.configuration.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            html_path = os.path.join(settings.PDF_TEMP_PATH, html_filename)
            
            logger.info("Создаю HTML файл как резервный вариант")
            html_content = self._generate_simple_html_report(export_data)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML файл создан: {html_path}")
            return html_path
    
    def _generate_simple_html_report(self, export_data: ConfigurationExport) -> str:
        """Генерация простого HTML отчета"""
        
        config = export_data.configuration
        compatibility = export_data.compatibility_check
        
        # Считаем общую стоимость
        total_price = sum((item.price_snapshot or item.component.price) * item.quantity for item in config.items)
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Конфигурация ПК - {config.name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 20px;
                }}
                .header h1 {{
                    color: #2563eb;
                    margin: 0;
                }}
                .section {{
                    margin-bottom: 25px;
                }}
                .section h2 {{
                    color: #1f2937;
                    border-left: 4px solid #2563eb;
                    padding-left: 12px;
                }}
                .component {{
                    background: #f9fafb;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 12px;
                    margin-bottom: 8px;
                }}
                .component-name {{
                    font-weight: bold;
                    color: #1f2937;
                }}
                .component-price {{
                    font-weight: bold;
                    color: #059669;
                }}
                .total {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2563eb;
                    text-align: center;
                    margin: 20px 0;
                    padding: 20px;
                    background: #f0f9ff;
                    border-radius: 8px;
                }}
                .compatibility {{
                    padding: 10px;
                    border-radius: 6px;
                    margin: 10px 0;
                }}
                .compatible {{ background: #d1fae5; color: #065f46; }}
                .warning {{ background: #fef3c7; color: #92400e; }}
                .incompatible {{ background: #fee2e2; color: #991b1b; }}
                .unknown {{ background: #f3f4f6; color: #374151; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Конфигурация ПК</h1>
                <h2>{config.name}</h2>
                {f'<p>{config.description}</p>' if config.description else ''}
                <p>Дата экспорта: {export_data.export_date.strftime('%d.%m.%Y %H:%M')}</p>
            </div>

            <div class="section">
                <h2>Компоненты</h2>
        """
        
        # Добавляем компоненты
        for item in config.items:
            price = item.price_snapshot or item.component.price
            html += f"""
                <div class="component">
                    <div class="component-name">{item.component.category.name}: {item.component.brand} {item.component.name}</div>
                    <div>Модель: {item.component.model}</div>
                    <div>Количество: {item.quantity}</div>
                    <div class="component-price">Цена: {price:,.0f} руб.</div>
                </div>
            """
        
        html += f"""
            </div>

            <div class="total">
                Общая стоимость: {total_price:,.0f} руб.
            </div>

            <div class="section">
                <h2>Совместимость</h2>
                <div class="compatibility {compatibility.status.lower()}">
                    Статус: {self._get_compatibility_status_text(compatibility.status)}
                </div>
                {f'<p>Общее энергопотребление: {compatibility.total_power_consumption} Вт</p>' if compatibility.total_power_consumption else ''}
                {f'<p>Рекомендуемая мощность БП: {compatibility.recommended_psu_wattage} Вт</p>' if compatibility.recommended_psu_wattage else ''}
        """
        
        # Добавляем проблемы совместимости
        if compatibility.issues:
            html += "<h3>Проблемы совместимости:</h3>"
            for issue in compatibility.issues:
                html += f"""
                    <div class="compatibility {issue.severity}">
                        <strong>{issue.type} ({issue.severity}):</strong> {issue.message}
                        {f'<br><em>Рекомендации: {", ".join(issue.suggestions)}</em>' if issue.suggestions else ''}
                    </div>
                """
        
        html += """
            </div>

            <div style="text-align: center; margin-top: 40px; font-size: 12px; color: #9ca3af;">
                <p>Конфигурация создана с помощью веб-конфигуратора ПК</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
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
        total_price = sum((item.price_snapshot or item.component.price) * item.quantity for item in config.items)
        
        # Создаем таблицу с общей информацией
        info_data = [
            ['ОБЩАЯ СТОИМОСТЬ', f'{total_price:,.0f} ₽'.replace(',', ' ')],
            ['СТАТУС СОВМЕСТИМОСТИ', self._get_compatibility_status_text(compatibility.status)],
        ]
        
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