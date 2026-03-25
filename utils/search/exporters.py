# -*- coding: utf-8 -*-

"""Экспорт результатов поиска"""
from typing import List
from database.models import Client
from datetime import datetime


class SearchExporter:
    """Класс для экспорта результатов поиска"""
    
    @staticmethod
    def to_txt(clients: List[Client]) -> str:
        """
        Экспорт в текстовый формат
        
        Args:
            clients: список клиентов
            
        Returns:
            str: отформатированный текст
        """
        lines = [
            f"Результаты поиска ({len(clients)} клиентов)",
            f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            "=" * 60,
            ""
        ]
        
        for i, client in enumerate(clients, 1):
            status = "✅" if client.is_completed else "⬜"
            lines.append(f"{i}. {status} {client.name}")
            lines.append(f"   📱 Telegram: @{client.telegram or '—'}")
            lines.append(f"   📞 Телефон: {client.phone or '—'}")
            lines.append(f"   📅 Дата рождения: {client.birth_date}")
            lines.append(f"   🔢 Число судьбы: {client.destiny_number}")
            lines.append(f"   📊 Матрица: {client.matrix_name or '—'}")
            lines.append(f"   💰 Цена: {client.service_price:,.0f} ₽".replace(",", " "))
            lines.append(f"   📅 Дата заказа: {client.order_date}")
            if client.comment:
                lines.append(f"   💬 Комментарий: {client.comment}")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_csv(clients: List[Client]) -> str:
        """
        Экспорт в CSV формат
        
        Args:
            clients: список клиентов
            
        Returns:
            str: CSV строка
        """
        lines = ["ID;Имя;Telegram;Телефон;Дата рождения;Число;Матрица;Цена;Дата заказа;Статус;Комментарий"]
        
        for client in clients:
            status = "Выполнен" if client.is_completed else "В ожидании"
            line = (
                f"{client.id};"
                f"{client.name};"
                f"{client.telegram or ''};"
                f"{client.phone or ''};"
                f"{client.birth_date};"
                f"{client.destiny_number};"
                f"{client.matrix_name or ''};"
                f"{client.service_price};"
                f"{client.order_date};"
                f"{status};"
                f"{client.comment or ''}"
            )
            lines.append(line)
        
        return "\n".join(lines)
    
    @staticmethod
    def to_json(clients: List[Client]) -> str:
        """
        Экспорт в JSON формат
        
        Args:
            clients: список клиентов
            
        Returns:
            str: JSON строка
        """
        import json
        
        data = []
        for client in clients:
            data.append({
                'id': client.id,
                'name': client.name,
                'telegram': client.telegram,
                'phone': client.phone,
                'birth_date': client.birth_date,
                'destiny_number': client.destiny_number,
                'matrix': client.matrix_name,
                'price': client.service_price,
                'order_date': client.order_date,
                'completed': client.is_completed,
                'comment': client.comment
            })
        
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @staticmethod
    def to_html(clients: List[Client]) -> str:
        """
        Экспорт в HTML формат
        
        Args:
            clients: список клиентов
            
        Returns:
            str: HTML строка
        """
        html = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="UTF-8">',
            '<title>Результаты поиска</title>',
            '<style>',
            'body { font-family: Arial, sans-serif; margin: 20px; }',
            'h1 { color: #2b5e8c; }',
            'table { border-collapse: collapse; width: 100%; }',
            'th { background-color: #2b5e8c; color: white; padding: 10px; }',
            'td { border: 1px solid #ddd; padding: 8px; }',
            'tr:nth-child(even) { background-color: #f2f2f2; }',
            '.completed { background-color: #e8f5e8; }',
            '</style>',
            '</head>',
            '<body>',
            f'<h1>Результаты поиска ({len(clients)} клиентов)</h1>',
            f'<p>Дата экспорта: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>',
            '<table>',
            '<tr>',
            '<th>ID</th>',
            '<th>Имя</th>',
            '<th>Telegram</th>',
            '<th>Телефон</th>',
            '<th>Дата рожд.</th>',
            '<th>Число</th>',
            '<th>Матрица</th>',
            '<th>Цена</th>',
            '<th>Дата заказа</th>',
            '<th>Статус</th>',
            '</tr>'
        ]
        
        for client in clients:
            row_class = 'completed' if client.is_completed else ''
            html.append(f'<tr class="{row_class}">')
            from html import escape as _esc
            html.append(f'<td>{_esc(str(client.id))}</td>')
            html.append(f'<td>{_esc(client.name)}</td>')
            html.append(f'<td>@{_esc(client.telegram or "")}</td>')
            html.append(f'<td>{_esc(client.phone or "")}</td>')
            html.append(f'<td>{_esc(client.birth_date)}</td>')
            html.append(f'<td>{_esc(str(client.destiny_number))}</td>')
            html.append(f'<td>{_esc(client.matrix_name or "")}</td>')
            html.append(f'<td>{client.service_price:,.0f} ₽</td>'.replace(",", " "))
            html.append(f'<td>{_esc(client.order_date)}</td>')
            html.append(f'<td>{"✅" if client.is_completed else "⬜"}</td>')
            html.append('</tr>')
        
        html.extend([
            '</table>',
            '</body>',
            '</html>'
        ])
        
        return "\n".join(html)


# Создаем глобальный экземпляр
exporter = SearchExporter()