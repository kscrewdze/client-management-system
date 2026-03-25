# -*- coding: utf-8 -*-

"""Рубиновая тема — тёплые бордовые акценты"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class RubyTheme(BaseTheme):
    """Рубиновая тема"""

    def __init__(self):
        self.name = "Рубиновая"
        self.description = "Тёплые бордовые акценты"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#c62828",
            secondary="#d32f2f",
            accent="#ffd54f",
            success="#2e7d32",
            warning="#fb8c00",
            error="#b71c1c",
            info="#0288d1",
            background="#fdf5f5",
            background_secondary="#fce8e8",
            background_widget="#ffffff",
            background_hover="#f5cece",
            text_primary="#3e1010",
            text_secondary="#7b3535",
            text_accent="#bf360c",
            text_disabled="#a0a0a0",
            text_inverse="#ffffff",
            border="#e8b4b4",
            border_focus="#c62828",
            highlight="#ef5350",
            shadow="#ffcdd2",
        )


ruby = RubyTheme()