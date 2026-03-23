# -*- coding: utf-8 -*-

"""Базовый фрейм для выбора тем"""
import customtkinter as ctk
from widgets.notifications import NotificationLabel
from gui.frames.settings.themes_section import ThemesSection


class ThemesFrame(ctk.CTkFrame):
    """Фрейм для выбора тем"""
    
    def __init__(self, parent, notifier: NotificationLabel, db=None):
        super().__init__(parent, fg_color="transparent")
        self.notifier = notifier
        self.db = db
        
        # Инициализация секции тем
        self.themes_section = ThemesSection(self, notifier)
        
        self.create_widgets()
        print("✅ ThemesFrame инициализирован")
    
    def create_widgets(self):
        """Создание виджетов"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🎨 ВЫБОР ТЕМЫ",
            font=("Segoe UI", 22, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(pady=25)
        
        # Центрируем карточку
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Карточка с темами по центру
        self.themes_section.create_centered(center_frame)