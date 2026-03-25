# -*- coding: utf-8 -*-

"""Полуночная тема — тёмная с мягкими голубыми акцентами"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class MidnightTheme(BaseTheme):
    """Полуночная тема"""

    def __init__(self):
        self.name = "Полуночная"
        self.description = "Тёмная с голубыми акцентами"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#82b1ff",
            secondary="#448aff",
            accent="#ffd740",
            success="#69f0ae",
            warning="#ffab40",
            error="#ff5252",
            info="#40c4ff",
            background="#181c24",
            background_secondary="#1e2530",
            background_widget="#252d3a",
            background_hover="#2f3a4a",
            text_primary="#e0e6ef",
            text_secondary="#8899aa",
            text_accent="#ffd740",
            text_disabled="#4a5568",
            text_inverse="#181c24",
            border="#2f3a4a",
            border_focus="#82b1ff",
            highlight="#448aff",
            shadow="#0d1017",
        )


midnight = MidnightTheme()