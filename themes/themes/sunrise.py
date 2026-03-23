# -*- coding: utf-8 -*-

"""Рассветная тема - теплые оранжево-розовые тона"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class SunriseTheme(BaseTheme):
    """Рассветная тема"""
    
    def __init__(self):
        self.name = "Рассветная"
        self.description = "Теплые оранжево-розовые тона"
        super().__init__()
    
    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#ff6f00",
            secondary="#ff8f00",
            accent="#4fc3f7",
            success="#2e7d32",
            warning="#ff9800",
            error="#d32f2f",
            info="#0288d1",
            background="#fff3e0",
            background_secondary="#ffe0b2",
            background_widget="#ffffff",
            background_hover="#ffcc80",
            text_primary="#bf360c",
            text_secondary="#e65100",
            text_accent="#0277bd",
            text_disabled="#9e9e9e",
            text_inverse="#ffffff",
            border="#ffb74d",
            border_focus="#ff9800",
            highlight="#ffa726",
            shadow="#ffe0b2"
        )


sunrise = SunriseTheme()