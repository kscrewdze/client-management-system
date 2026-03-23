# -*- coding: utf-8 -*-

"""Стили для диалоговых окон"""
import customtkinter as ctk


class DialogStyles:
    """Класс с настройками стилей для диалогов"""
    
    # Размеры
    WIDTH_SMALL = 350
    WIDTH_MEDIUM = 400
    WIDTH_LARGE = 450
    
    HEIGHT_SMALL = 200
    HEIGHT_MEDIUM = 250
    HEIGHT_LARGE = 300
    
    # Цвета
    COLOR_PRIMARY = "#2b5e8c"
    COLOR_SUCCESS = "#2e7d32"
    COLOR_WARNING = "#ed6c02"
    COLOR_ERROR = "#d32f2f"
    COLOR_INFO = "#0288d1"
    COLOR_GRAY = "#757575"
    
    # Шрифты
    FONT_TITLE = ("Segoe UI", 14, "bold")
    FONT_NORMAL = ("Segoe UI", 11)
    FONT_SMALL = ("Segoe UI", 10)
    FONT_HINT = ("Segoe UI", 9)
    
    # Отступы
    PADX = 20
    PADY = 15
    
    @classmethod
    def configure(cls):
        """Настройка глобальных стилей"""
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")