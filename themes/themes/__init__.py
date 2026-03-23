# -*- coding: utf-8 -*-

"""Пакет с темами"""
from themes.themes.base_theme import BaseTheme, ThemeColors
from themes.themes.emerald import emerald
from themes.themes.sapphire import sapphire
from themes.themes.ruby import ruby
from themes.themes.amethyst import amethyst
from themes.themes.midnight import midnight
from themes.themes.sunrise import sunrise

__all__ = [
    'BaseTheme', 'ThemeColors',
    'emerald', 'sapphire', 'ruby',
    'amethyst', 'midnight', 'sunrise'
]