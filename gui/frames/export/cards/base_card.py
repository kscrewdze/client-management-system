# -*- coding: utf-8 -*-

"""Базовый класс для карточек экспорта"""
import customtkinter as ctk
from widgets.tooltip import ToolTip


class BaseExportCard:
    """Базовый класс карточки экспорта"""
    
    def __init__(self, parent, title, subtitle, description, color, emoji, command, column):
        """
        Инициализация базовой карточки
        
        Args:
            parent: родительский фрейм
            title: заголовок карточки
            subtitle: подзаголовок
            description: описание
            color: цвет карточки
            emoji: эмодзи
            command: функция для экспорта
            column: колонка в сетке
        """
        self.parent = parent
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.color = color
        self.emoji = emoji
        self.command = command
        self.column = column
        
        self.create_card()
    
    def create_card(self):
        """Создание карточки"""
        card = ctk.CTkFrame(
            self.parent,
            width=260,
            height=220,
            corner_radius=12,
            border_width=2,
            border_color=self.color
        )
        card.grid(row=0, column=self.column, padx=12, pady=5)
        card.grid_propagate(False)
        
        # Внутренний контейнер
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Эмодзи
        emoji_label = ctk.CTkLabel(
            inner,
            text=self.emoji,
            font=("Segoe UI", 40),
            text_color=self.color
        )
        emoji_label.pack(pady=(0, 2))
        
        # Заголовок
        title_label = ctk.CTkLabel(
            inner,
            text=self.title,
            font=("Segoe UI", 16, "bold"),
            text_color=self.color
        )
        title_label.pack()
        
        # Подзаголовок
        subtitle_label = ctk.CTkLabel(
            inner,
            text=self.subtitle,
            font=("Segoe UI", 10),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Описание
        desc_label = ctk.CTkLabel(
            inner,
            text=self.description,
            font=("Segoe UI", 9),
            text_color="#666666",
            justify="center",
            wraplength=220
        )
        desc_label.pack(pady=2)
        
        # Кнопка
        btn = ctk.CTkButton(
            inner,
            text="📥 Экспортировать",
            command=self.command,
            width=140,
            height=30,
            font=("Segoe UI", 10, "bold"),
            fg_color=self.color,
            hover_color=self._darken_color(self.color),
            corner_radius=6
        )
        btn.pack(pady=5)
        
        ToolTip(btn, f"Экспортировать в {self.title}")
    
    def _darken_color(self, color):
        """Затемнение цвета для hover эффекта"""
        darken_map = {
            "#217346": "#1a5c38",
            "#f7df1e": "#e5cb14",
        }
        return darken_map.get(color, color)