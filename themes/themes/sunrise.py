# -*- coding: utf-8 -*-

"""Рассветная тема — тёплые солнечные тона"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class SunriseTheme(BaseTheme):
    """Рассветная тема"""

    def __init__(self):
        self.name = "Рассветная"
        self.description = "Тёплые солнечные тона"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#ef6c00",
            secondary="#f57c00",
            accent="#039be5",
            success="#2e7d32",
            warning="#ffa000",
            error="#e53935",
            info="#0288d1",
            background="#fffaf4",
            background_secondary="#fff3e0",
            background_widget="#ffffff",
            background_hover="#ffe8cc",
            text_primary="#3e2110",
            text_secondary="#8b5e3c",
            text_accent="#0277bd",
            text_disabled="#a0a0a0",
            text_inverse="#ffffff",
            border="#ffe0b2",
            border_focus="#ef6c00",
            highlight="#ffa726",
            shadow="#ffcc80",
        )


sunrise = SunriseTheme()