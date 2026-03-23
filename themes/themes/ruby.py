# -*- coding: utf-8 -*-

"""Рубиновая тема - красные оттенки"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class RubyTheme(BaseTheme):
    """Рубиновая тема"""
    
    def __init__(self):
        self.name = "Рубиновая"
        self.description = "Красные оттенки"
        super().__init__()
    
    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#b71c1c",
            secondary="#d32f2f",
            accent="#ffd54f",
            success="#2e7d32",
            warning="#ff9800",
            error="#f44336",
            info="#0288d1",
            background="#ffebee",
            background_secondary="#ffcdd2",
            background_widget="#ffffff",
            background_hover="#ef9a9a",
            text_primary="#b71c1c",
            text_secondary="#c62828",
            text_accent="#ffd54f",
            text_disabled="#9e9e9e",
            text_inverse="#ffffff",
            border="#ef5350",
            border_focus="#d32f2f",
            highlight="#e57373",
            shadow="#ffcdd2"
        )


ruby = RubyTheme()