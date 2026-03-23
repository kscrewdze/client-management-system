# -*- coding: utf-8 -*-

"""Изумрудная тема - свежие зеленые оттенки"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class EmeraldTheme(BaseTheme):
    """Изумрудная тема"""
    
    def __init__(self):
        self.name = "Изумрудная"
        self.description = "Свежие зеленые оттенки"
        super().__init__()
    
    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#2e7d32",
            secondary="#1b5e20",
            accent="#ffb74d",
            success="#4caf50",
            warning="#ff9800",
            error="#f44336",
            info="#00bcd4",
            background="#f1f8e9",
            background_secondary="#e8f5e9",
            background_widget="#ffffff",
            background_hover="#c8e6c9",
            text_primary="#1b5e20",
            text_secondary="#2e7d32",
            text_accent="#ff6d00",
            text_disabled="#9e9e9e",
            text_inverse="#ffffff",
            border="#a5d6a7",
            border_focus="#2e7d32",
            highlight="#66bb6a",
            shadow="#81c784"
        )


emerald = EmeraldTheme()