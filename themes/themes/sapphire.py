# -*- coding: utf-8 -*-

"""Сапфировая тема — глубокие синие тона, деловой стиль"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class SapphireTheme(BaseTheme):
    """Сапфировая тема"""

    def __init__(self):
        self.name = "Сапфировая"
        self.description = "Деловой синий стиль"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#1565c0",
            secondary="#1976d2",
            accent="#ffa726",
            success="#2e7d32",
            warning="#fb8c00",
            error="#e53935",
            info="#0288d1",
            background="#f4f7fb",
            background_secondary="#e8eef6",
            background_widget="#ffffff",
            background_hover="#d6e4f0",
            text_primary="#102a4c",
            text_secondary="#446189",
            text_accent="#e65100",
            text_disabled="#a0a0a0",
            text_inverse="#ffffff",
            border="#b0c4de",
            border_focus="#1565c0",
            highlight="#42a5f5",
            shadow="#90caf9",
        )


sapphire = SapphireTheme()