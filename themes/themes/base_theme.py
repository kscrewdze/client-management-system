# -*- coding: utf-8 -*-

"""Базовый класс для всех тем"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ThemeColors:
    """Класс с цветами темы"""
    
    # Основные цвета
    primary: str
    secondary: str
    accent: str
    success: str
    warning: str
    error: str
    info: str
    
    # Фоны
    background: str          # Основной фон
    background_secondary: str # Вторичный фон
    background_widget: str   # Фон виджетов
    background_hover: str    # Фон при наведении
    
    # Текст
    text_primary: str        # Основной текст
    text_secondary: str      # Вторичный текст
    text_accent: str         # Акцентный текст
    text_disabled: str       # Неактивный текст
    text_inverse: str        # Текст на темном фоне
    
    # Границы
    border: str
    border_focus: str
    
    # Специальные
    highlight: str
    shadow: str


class BaseTheme:
    """Базовый класс темы"""
    
    def __init__(self):
        self.name = "Base Theme"
        self.description = "Базовая тема"
        self.colors = self.get_colors()
        self.fonts = self.get_fonts()
        self.sizes = self.get_sizes()
    
    def get_colors(self) -> ThemeColors:
        """Получить цвета темы"""
        return ThemeColors(
            primary="#2b5e8c",
            secondary="#1e3f5c",
            accent="#ff6b6b",
            success="#2e7d32",
            warning="#ed6c02",
            error="#d32f2f",
            info="#0288d1",
            background="#f5f5f5",
            background_secondary="#ffffff",
            background_widget="#ffffff",
            background_hover="#e0e0e0",
            text_primary="#000000",
            text_secondary="#4a4a4a",
            text_accent="#d32f2f",
            text_disabled="#9e9e9e",
            text_inverse="#ffffff",
            border="#e0e0e0",
            border_focus="#2b5e8c",
            highlight="#2b5e8c",
            shadow="#cccccc"
        )
    
    def get_fonts(self) -> Dict:
        """Получить настройки шрифтов"""
        return {
            'title': ("Segoe UI", 18, "bold"),
            'heading': ("Segoe UI", 14, "bold"),
            'normal': ("Segoe UI", 11),
            'small': ("Segoe UI", 10),
            'hint': ("Segoe UI", 9)
        }
    
    def get_sizes(self) -> Dict:
        """Получить размеры"""
        return {
            'window_width': 1000,
            'window_height': 600,
            'border_radius': 15,
            'button_height': 36,
            'entry_height': 30,
            'padding': 10,
            'spacing': 5
        }