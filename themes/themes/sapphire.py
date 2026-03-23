# -*- coding: utf-8 -*-

"""Сапфировая тема - глубокие синие тона"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class SapphireTheme(BaseTheme):
    """Сапфировая тема"""
    
    def __init__(self):
        self.name = "Сапфировая"
        self.description = "Глубокие синие тона"
        super().__init__()
    
    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#0d47a1",
            secondary="#1565c0",
            accent="#ffb74d",
            success="#2e7d32",
            warning="#ed6c02",
            error="#d32f2f",
            info="#0288d1",
            background="#e3f2fd",
            background_secondary="#bbdefb",
            background_widget="#ffffff",
            background_hover="#90caf9",
            text_primary="#0d47a1",
            text_secondary="#1565c0",
            text_accent="#ff6d00",
            text_disabled="#9e9e9e",
            text_inverse="#ffffff",
            border="#64b5f6",
            border_focus="#1976d2",
            highlight="#42a5f5",
            shadow="#bbdefb"
        )


sapphire = SapphireTheme()