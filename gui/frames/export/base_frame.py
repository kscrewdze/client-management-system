# -*- coding: utf-8 -*-

"""Базовый фрейм для экспорта данных"""
import customtkinter as ctk
from database import Database
from widgets.notifications import NotificationLabel

from gui.frames.export.cards.excel_card import ExcelCard
from gui.frames.export.cards.json_card import JsonCard
from gui.frames.export.info_section import InfoSection
from gui.frames.export.exporters.excel_exporter import ExcelExporter
from gui.frames.export.exporters.json_exporter import JsonExporter


class ExportFrame(ctk.CTkFrame):
    """Фрейм для экспорта данных"""
    
    def __init__(self, parent, db: Database, notifier: NotificationLabel):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.notifier = notifier
        
        # Инициализация экспортеров
        self.excel_exporter = ExcelExporter(db, notifier)
        self.json_exporter = JsonExporter(db, notifier)
        
        # Информационная секция
        self.info_section = InfoSection(self, notifier)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="📊 ЭКСПОРТ ДАННЫХ",
            font=("Segoe UI", 22, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(pady=(15, 15))
        
        # Контейнер для карточек
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(expand=True, fill="both", padx=40)
        
        # Центрируем карточки
        center_frame = ctk.CTkFrame(cards_container, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Excel карточка
        ExcelCard(
            center_frame,
            self.export_excel,
            column=0
        )
        
        # JSON карточка
        JsonCard(
            center_frame,
            self.export_json,
            column=1
        )
        
        # Информационная секция
        self.info_section.create()
    
    def export_excel(self):
        """Экспорт в Excel"""
        result = self.excel_exporter.export()
        if result:
            self.info_section.update_stats()  # Мгновенное обновление
        return result
    
    def export_json(self):
        """Экспорт в JSON"""
        result = self.json_exporter.export()
        if result:
            self.info_section.update_stats()  # Мгновенное обновление
        return result
    
    def cancel_updates(self):
        """Отмена обновлений при закрытии"""
        if hasattr(self, 'info_section'):
            self.info_section.cancel_updates()