# -*- coding: utf-8 -*-

"""Пакет тем для приложения"""
from themes.themes import BaseTheme, ThemeColors
from themes.themes import emerald, sapphire, ruby, amethyst, midnight, sunrise
from themes.manager import theme_manager, ThemeManager

__all__ = [
    'BaseTheme', 'ThemeColors',
    'ThemeManager', 'theme_manager',
    'emerald', 'sapphire', 'ruby',
    'amethyst', 'midnight', 'sunrise'
]