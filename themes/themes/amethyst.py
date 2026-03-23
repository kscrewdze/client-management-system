# -*- coding: utf-8 -*-

"""Аметистовая тема - фиолетовые оттенки"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class AmethystTheme(BaseTheme):
    """Аметистовая тема"""
    
    def __init__(self):
        self.name = "Аметистовая"
        self.description = "Фиолетовые оттенки"
        super().__init__()
    
    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#4a148c",
            secondary="#6a1b9a",
            accent="#ffd54f",
            success="#2e7d32",
            warning="#ff9800",
            error="#d32f2f",
            info="#0288d1",
            background="#f3e5f5",
            background_secondary="#e1bee7",
            background_widget="#ffffff",
            background_hover="#ce93d8",
            text_primary="#4a148c",
            text_secondary="#6a1b9a",
            text_accent="#ffd54f",
            text_disabled="#9e9e9e",
            text_inverse="#ffffff",
            border="#ba68c8",
            border_focus="#7b1fa2",
            highlight="#ab47bc",
            shadow="#e1bee7"
        )


amethyst = AmethystTheme()