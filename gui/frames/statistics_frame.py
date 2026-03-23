# -*- coding: utf-8 -*-

"""Фрейм со статистикой"""
from datetime import datetime
import customtkinter as ctk

from database import Database
from widgets.notifications import NotificationLabel
from themes import theme_manager  # ИСПРАВЛЕНО: было from themes.themes import theme_manager


class StatisticsFrame(ctk.CTkFrame):
    """Фрейм со статистикой"""
    
    def __init__(self, parent, db: Database, notifier: NotificationLabel):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.notifier = notifier
        self.stats_cards = {}
        self.create_widgets()
        self.refresh()
    
    def create_widgets(self):
        """Создание виджетов"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="📊 СТАТИСТИКА",
            font=("Segoe UI", 16, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(pady=(5, 10))
        
        # Сетка карточек
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=10)
        
        # Настройка сетки
        for i in range(2):
            self.cards_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        # Создание карточек статистики
        stats = [
            ("👥 Всего клиентов", "total_clients", "#2b5e8c"),
            ("💰 Общий заработок", "total_earnings", "#2e7d32"),
            ("📊 Средний чек", "average_price", "#ed6c02"),
            ("✅ Выполнено", "completed_count", "#0288d1"),
            ("💵 Заработано (вып.)", "completed_earnings", "#9c27b0"),
            ("📋 Матриц", "matrices_count", "#795548")
        ]
        
        for i, (title, key, color) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            card = self.create_stat_card(title, key, color)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Кнопка обновления
        refresh_btn = ctk.CTkButton(
            self,
            text="🔄 Обновить",
            command=self.refresh,
            width=120,
            height=30,
            font=("Segoe UI", 11, "bold"),
            fg_color="#2e7d32",
            hover_color="#1e5a23"
        )
        refresh_btn.pack(pady=8)
    
    def create_stat_card(self, title: str, key: str, color: str) -> ctk.CTkFrame:
        """Создание карточки статистики"""
        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=color,
            corner_radius=8,
            height=80
        )
        card.pack_propagate(False)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(8, 2))
        
        # Значение
        value_label = ctk.CTkLabel(
            card,
            text="0",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        value_label.pack()
        
        self.stats_cards[key] = value_label
        
        return card
    
    def refresh(self):
        """Обновление статистики"""
        try:
            stats = self.db.get_statistics()
            
            # Обновление карточек
            self.stats_cards["total_clients"].configure(text=str(stats['total_clients']))
            self.stats_cards["total_earnings"].configure(text=f"{stats['total_earnings']:,.0f} ₽".replace(",", " "))
            self.stats_cards["average_price"].configure(text=f"{stats['average_price']:,.0f} ₽".replace(",", " "))
            self.stats_cards["completed_count"].configure(text=str(stats['completed_count']))
            self.stats_cards["completed_earnings"].configure(text=f"{stats['completed_earnings']:,.0f} ₽".replace(",", " "))
            self.stats_cards["matrices_count"].configure(text=str(stats['matrices_count']))
            
        except Exception as e:
            self.notifier.show_error(f"❌ Ошибка: {str(e)}")