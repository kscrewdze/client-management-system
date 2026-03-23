# -*- coding: utf-8 -*-

"""Полуночная тема - темная с контрастными акцентами"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class MidnightTheme(BaseTheme):
    """Полуночная тема"""
    
    def __init__(self):
        self.name = "Полуночная"
        self.description = "Темная тема с контрастными акцентами"
        super().__init__()
    
    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#90caf9",
            secondary="#64b5f6",
            accent="#ffb74d",
            success="#81c784",
            warning="#ffb74d",
            error="#e57373",
            info="#4fc3f7",
            background="#121212",
            background_secondary="#1e1e1e",
            background_widget="#2d2d2d",
            background_hover="#3d3d3d",
            text_primary="#ffffff",
            text_secondary="#b0b0b0",
            text_accent="#ffb74d",
            text_disabled="#666666",
            text_inverse="#000000",
            border="#3d3d3d",
            border_focus="#90caf9",
            highlight="#64b5f6",
            shadow="#000000"
        )


midnight = MidnightTheme()