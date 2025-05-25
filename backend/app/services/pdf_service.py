import os
import tempfile
from datetime import datetime
from typing import Optional
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader
from ..schemas.configuration import ConfigurationExport
from ..config import settings


class PDFService:
    """Сервис для генерации PDF отчетов"""
    
    def __init__(self):
        # Настройка Jinja2 для шаблонов
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_configuration_pdf(self, export_data: ConfigurationExport) -> str:
        """Генерация PDF отчета конфигурации"""
        
        # Создаем временный файл для PDF (пока что HTML)
        pdf_filename = f"config_{export_data.configuration.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        pdf_path = os.path.join(settings.PDF_TEMP_PATH, pdf_filename)
        
        # Генерируем простой HTML отчет
        html_content = self._generate_simple_html_report(export_data)
        
        # Сохраняем в файл
        os.makedirs(settings.PDF_TEMP_PATH, exist_ok=True)
        with open(pdf_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return pdf_path
    
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
    
    def _render_configuration_template(self, export_data: ConfigurationExport) -> str:
        """Рендер HTML шаблона конфигурации"""
        
        template = self.jinja_env.get_template("configuration_pdf.html")
        
        # Подготавливаем данные для шаблона
        config = export_data.configuration
        compatibility = export_data.compatibility_check
        
        # Группируем компоненты по категориям
        components_by_category = {}
        total_price = 0.0
        
        for item in config.items:
            category = item.component.category.name
            if category not in components_by_category:
                components_by_category[category] = []
            
            price = item.price_snapshot or item.component.price
            total_price += price * item.quantity
            
            components_by_category[category].append({
                "name": item.component.name,
                "brand": item.component.brand,
                "model": item.component.model,
                "price": price,
                "quantity": item.quantity,
                "total": price * item.quantity,
                "stock_status": self._get_stock_status_text(item.component.stock.status) if item.component.stock else "Неизвестно",
                "specifications": self._format_specifications(item.component.specifications)
            })
        
        # Форматируем проблемы совместимости
        compatibility_issues = []
        for issue in compatibility.issues:
            compatibility_issues.append({
                "type": self._get_issue_type_text(issue.type),
                "severity": self._get_severity_text(issue.severity),
                "message": issue.message,
                "suggestions": issue.suggestions or []
            })
        
        template_data = {
            "config": config,
            "components_by_category": components_by_category,
            "total_price": total_price,
            "compatibility_status": self._get_compatibility_status_text(compatibility.status),
            "compatibility_issues": compatibility_issues,
            "total_power": compatibility.total_power_consumption,
            "recommended_psu": compatibility.recommended_psu_wattage,
            "export_date": export_data.export_date.strftime("%d.%m.%Y %H:%M"),
            "notes": export_data.notes
        }
        
        return template.render(**template_data)
    
    def _get_pdf_styles(self) -> CSS:
        """Получить CSS стили для PDF"""
        
        css_content = """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
        }
        
        .header h1 {
            color: #2563eb;
            margin: 0;
            font-size: 24px;
            font-weight: 700;
        }
        
        .header p {
            color: #666;
            margin: 5px 0;
        }
        
        .section {
            margin-bottom: 25px;
        }
        
        .section h2 {
            color: #1f2937;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            border-left: 4px solid #2563eb;
            padding-left: 12px;
        }
        
        .category {
            margin-bottom: 20px;
        }
        
        .category h3 {
            color: #374151;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .component {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
        }
        
        .component-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .component-name {
            font-weight: 600;
            color: #1f2937;
        }
        
        .component-price {
            font-weight: 600;
            color: #059669;
        }
        
        .component-details {
            font-size: 14px;
            color: #6b7280;
        }
        
        .compatibility-status {
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: 500;
            display: inline-block;
        }
        
        .compatible {
            background-color: #d1fae5;
            color: #065f46;
        }
        
        .warning {
            background-color: #fef3c7;
            color: #92400e;
        }
        
        .incompatible {
            background-color: #fee2e2;
            color: #991b1b;
        }
        
        .issue {
            background: #fef2f2;
            border-left: 4px solid #f87171;
            padding: 10px;
            margin: 8px 0;
        }
        
        .issue.warning {
            background: #fffbeb;
            border-left-color: #f59e0b;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        
        .summary-item {
            text-align: center;
        }
        
        .summary-value {
            font-size: 20px;
            font-weight: 700;
            color: #2563eb;
        }
        
        .summary-label {
            font-size: 14px;
            color: #6b7280;
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            color: #9ca3af;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        
        th {
            background-color: #f3f4f6;
            font-weight: 600;
        }
        """
        
        return CSS(string=css_content)
    
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