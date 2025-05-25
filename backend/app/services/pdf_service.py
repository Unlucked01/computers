import os
import tempfile
import logging
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
            self._generate_pdf_with_reportlab(export_data, pdf_path)
            
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

    def _generate_pdf_with_reportlab(self, export_data: ConfigurationExport, pdf_path: str):
        """Генерация PDF с помощью reportlab"""
        
        config = export_data.configuration
        compatibility = export_data.compatibility_check
        
        # Создаем документ
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        # Получаем стили
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Центрирование
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2563eb')
        )
        
        # Заголовок
        story.append(Paragraph("Конфигурация ПК", title_style))
        story.append(Paragraph(f"<b>{config.name}</b>", styles['Normal']))
        if config.description:
            story.append(Paragraph(config.description, styles['Normal']))
        story.append(Paragraph(f"Дата экспорта: {export_data.export_date.strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Общая информация
        total_price = sum((item.price_snapshot or item.component.price) * item.quantity for item in config.items)
        
        story.append(Paragraph("Общая информация", heading_style))
        info_data = [
            ['Общая стоимость:', f'{total_price:,.0f} руб.'],
            ['Статус совместимости:', self._get_compatibility_status_text(compatibility.status)],
        ]
        
        if compatibility.total_power_consumption:
            info_data.append(['Энергопотребление:', f'{compatibility.total_power_consumption} Вт'])
        if compatibility.recommended_psu_wattage:
            info_data.append(['Рекомендуемая мощность БП:', f'{compatibility.recommended_psu_wattage} Вт'])
        
        info_table = Table(info_data, colWidths=[3*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Компоненты
        story.append(Paragraph("Компоненты", heading_style))
        
        # Группируем компоненты по категориям
        components_by_category = {}
        for item in config.items:
            category = item.component.category.name
            if category not in components_by_category:
                components_by_category[category] = []
            components_by_category[category].append(item)
        
        for category, items in components_by_category.items():
            story.append(Paragraph(f"<b>{category}</b>", styles['Heading3']))
            
            for item in items:
                price = item.price_snapshot or item.component.price
                component_text = f"""
                <b>{item.component.brand} {item.component.name}</b><br/>
                Модель: {item.component.model}<br/>
                Количество: {item.quantity}<br/>
                Цена: {price:,.0f} руб.
                """
                story.append(Paragraph(component_text, styles['Normal']))
                story.append(Spacer(1, 10))
        
        # Проблемы совместимости
        if compatibility.issues:
            story.append(Paragraph("Проблемы совместимости", heading_style))
            for issue in compatibility.issues:
                issue_text = f"""
                <b>{self._get_issue_type_text(issue.type)} ({self._get_severity_text(issue.severity)})</b><br/>
                {issue.message}
                """
                if issue.suggestions:
                    issue_text += f"<br/>Рекомендации: {', '.join(issue.suggestions)}"
                
                story.append(Paragraph(issue_text, styles['Normal']))
                story.append(Spacer(1, 10))
        
        # Футер
        story.append(Spacer(1, 30))
        story.append(Paragraph("Конфигурация создана с помощью веб-конфигуратора ПК", styles['Normal']))
        if config.public_uuid:
            story.append(Paragraph(f"UUID: {config.public_uuid}", styles['Normal']))
        
        # Генерируем PDF
        doc.build(story) 