# -*- coding: utf-8 -*-

"""Аметистовая тема — мягкие фиолетово-лавандовые тона"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class AmethystTheme(BaseTheme):
    """Аметистовая тема"""

    def __init__(self):
        self.name = "Аметистовая"
        self.description = "Лавандовые тона"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#6a1b9a",
            secondary="#7b1fa2",
            accent="#ffa726",
            success="#2e7d32",
            warning="#fb8c00",
            error="#e53935",
            info="#0288d1",
            background="#f8f4fb",
            background_secondary="#f0e6f6",
            background_widget="#ffffff",
            background_hover="#e1d0eb",
            text_primary="#2a0845",
            text_secondary="#6a4c8a",
            text_accent="#e65100",
            text_disabled="#a0a0a0",
            text_inverse="#ffffff",
            border="#d1b3e0",
            border_focus="#6a1b9a",
            highlight="#ab47bc",
            shadow="#ce93d8",
        )


amethyst = AmethystTheme()