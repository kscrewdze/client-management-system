# -*- coding: utf-8 -*-

"""Стеклянная тема — полупрозрачный эффект"""
from themes.themes.base_theme import BaseTheme, ThemeColors


class GlassTheme(BaseTheme):
    """Полупрозрачная стеклянная тема"""

    def __init__(self):
        self.name = "Стеклянная"
        self.description = "Полупрозрачный эффект, лёгкость"
        super().__init__()

    def get_colors(self) -> ThemeColors:
        return ThemeColors(
            primary="#5c6bc0",
            secondary="#7986cb",
            accent="#26c6da",
            success="#66bb6a",
            warning="#ffa726",
            error="#ef5350",
            info="#29b6f6",
            background="rgba(235,238,245,220)",
            background_secondary="rgba(225,228,240,200)",
            background_widget="rgba(255,255,255,180)",
            background_hover="rgba(210,215,230,200)",
            text_primary="#2c3e50",
            text_secondary="#607d8b",
            text_accent="#1a237e",
            text_disabled="#b0bec5",
            text_inverse="#ffffff",
            border="rgba(180,190,210,150)",
            border_focus="#5c6bc0",
            highlight="rgba(92,107,192,180)",
            shadow="rgba(0,0,0,30)",
        )


glass = GlassTheme()
