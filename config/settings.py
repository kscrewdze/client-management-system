# -*- coding: utf-8 -*-

"""Настройки приложения
Автор: kScrewdze
Версия: 9.0
"""
import os
import sys
from pathlib import Path
from typing import List, Tuple


class Settings:
    """Глобальные настройки приложения"""
    
    # Пути
    BASE_DIR = Path(__file__).parent.parent
    
    if getattr(sys, 'frozen', False):
        APP_DIR = Path(sys.executable).parent
    else:
        APP_DIR = BASE_DIR
    
    DB_PATH = APP_DIR / "clients.db"
    EXPORTS_DIR = APP_DIR / "exports"
    
    # Настройки базы данных
    DB_NAME = "clients.db"
    
    # Настройки UI (ФИКСИРОВАННЫЙ РАЗМЕР)
    APP_TITLE = "🏢 Управление клиентами v9.0"
    APP_WIDTH = 1000
    APP_HEIGHT = 600
    APP_GEOMETRY = f"{APP_WIDTH}x{APP_HEIGHT}"
    APP_MIN_SIZE: Tuple[int, int] = (900, 550)
    
    # Цветовая схема
    PRIMARY_COLOR = "#2b5e8c"
    SUCCESS_COLOR = "#2e7d32"
    WARNING_COLOR = "#ed6c02"
    ERROR_COLOR = "#d32f2f"
    INFO_COLOR = "#0288d1"
    
    # Форматы даты
    DATE_FORMATS: List[str] = [
        "%d.%m.%Y", "%d.%m.%y",
        "%d/%m/%Y", "%d/%m/%y",
        "%d-%m-%Y", "%d-%m-%y",
        "%Y.%m.%d", "%Y/%m/%d", "%Y-%m-%d"
    ]
    
    # Создание необходимых папок
    @classmethod
    def ensure_directories(cls):
        """Создание необходимых директорий"""
        cls.EXPORTS_DIR.mkdir(exist_ok=True)