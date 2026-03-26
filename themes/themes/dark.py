# -*- coding: utf-8 -*-

"""Тёмная тема — глубокий чёрный с минимальными акцентами"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class DarkTheme(BaseTheme):
    """Тёмная тема"""

    def __init__(self):
        self.name = "Тёмная"
        self.description = "Глубокий чёрный, минимальные акценты"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#bb86fc",
            secondary="#985eff",
            accent="#03dac6",
            success="#00c853",
            warning="#ffab00",
            error="#cf6679",
            info="#03dac6",
            background="#121212",
            background_secondary="#1e1e1e",
            background_widget="#2c2c2c",
            background_hover="#333333",
            text_primary="#e1e1e1",
            text_secondary="#a0a0a0",
            text_accent="#03dac6",
            text_disabled="#555555",
            text_inverse="#121212",
            border="#333333",
            border_focus="#bb86fc",
            highlight="#bb86fc",
            shadow="#000000",
        )


dark = DarkTheme()
