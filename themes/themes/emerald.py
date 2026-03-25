# -*- coding: utf-8 -*-

"""Изумрудная тема — элегантные зеленые тона с мягким контрастом"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class EmeraldTheme(BaseTheme):
    """Изумрудная тема"""

    def __init__(self):
        self.name = "Изумрудная"
        self.description = "Элегантные изумрудные тона"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#2e7d32",
            secondary="#388e3c",
            accent="#ffa726",
            success="#43a047",
            warning="#fb8c00",
            error="#e53935",
            info="#039be5",
            background="#f5f9f5",
            background_secondary="#eef5ee",
            background_widget="#ffffff",
            background_hover="#dcedc8",
            text_primary="#1b3a1b",
            text_secondary="#557a55",
            text_accent="#e65100",
            text_disabled="#a0a0a0",
            text_inverse="#ffffff",
            border="#c8e6c9",
            border_focus="#2e7d32",
            highlight="#66bb6a",
            shadow="#a5d6a7",
        )


emerald = EmeraldTheme()