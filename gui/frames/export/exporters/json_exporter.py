# -*- coding: utf-8 -*-

"""Экспорт в JSON с сохранением всех полей как в программе"""
import json
import os
from datetime import datetime
from gui.frames.export.exporters.base_exporter import BaseExporter


class JsonExporter(BaseExporter):
    """Экспортер в JSON с полными данными как в программе"""
    
    def export(self):
        """Экспорт в JSON"""
        try:
            # Проверка данных
            clients = self.check_data()
            if not clients:
                return
            
            # Преобразование в список словарей со всеми полями как в программе
            clients_data = []
            for client in clients:
                # Форматируем цену как в программе
                price_text = f"{client.service_price:,.0f} ₽".replace(",", " ")
                
                # Статус как в программе
                status = "✅ Выполнен" if client.is_completed else "⬜ В ожидании"
                status_emoji = "✅" if client.is_completed else "⬜"
                
                # Дата выполнения
                completed_display = ""
                if client.is_completed and client.completed_date:
                    completed_display = f"✅ {client.completed_date}"
                
                client_dict = {
                    'id': client.id,
                    'id_display': f"ID: {client.id}",
                    
                    'name': client.name,
                    'name_display': f"👤 {client.name}",
                    
                    'telegram': client.telegram,
                    'telegram_display': f"📱 {client.telegram}" if client.telegram else "📱 —",
                    
                    'phone': client.phone,
                    'phone_display': f"📞 {client.phone}" if client.phone else "📞 —",
                    
                    'birth_date': client.birth_date,
                    'birth_date_display': f"📅 {client.birth_date}",
                    
                    'destiny_number': client.destiny_number,
                    'destiny_display': f"🔢 {client.destiny_number}",
                    
                    'matrix': client.matrix_name,
                    'matrix_display': f"📊 {client.matrix_name}" if client.matrix_name else "📊 —",
                    
                    'price': client.service_price,
                    'price_display': f"💰 {price_text}",
                    
                    'order_date': client.order_date,
                    'order_date_display': f"📅 {client.order_date}",
                    
                    'status': status,
                    'status_emoji': status_emoji,
                    'is_completed': client.is_completed,
                    
                    'completed_date': client.completed_date,
                    'completed_display': completed_display,
                    
                    'comment': client.comment,
                    'comment_display': f"💬 {client.comment}" if client.comment else "💬 —",
                    
                    'created_date': client.created_date,
                    'created_date_display': f"📅 {client.created_date[:10]}" if client.created_date else "—"
                }
                clients_data.append(client_dict)
            
            # Создание структуры экспорта
            export_data = {
                'export_info': {
                    'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    'total_clients': len(clients),
                    'completed_count': sum(1 for c in clients if c.is_completed),
                    'total_earnings': sum(c.service_price for c in clients),
                    'format': 'Полный экспорт как в программе'
                },
                'clients': clients_data
            }
            
            # Создание файла
            filename = self.get_export_filename("json")
            
            # Сохранение в JSON с красивым форматированием
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            
            self.notifier.show_success(f"✅ Экспортировано {len(clients)} записей в JSON")
            
            # Спрашиваем, открыть ли папку
            if self.ask_open_folder(filename):
                self.open_export_folder()
            
            return filename
            
        except Exception as e:
            self.notifier.show_error(f"❌ Ошибка экспорта в JSON: {str(e)}")
            return None