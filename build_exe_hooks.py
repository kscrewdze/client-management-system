# -*- coding: utf-8 -*-

"""
Хуки для сборки .exe файла (PySide6 + PyInstaller).

Использование:
    pyinstaller --onefile --windowed --name ClientManager ^
        --add-data "themes;themes" ^
        --add-data "config;config" ^
        --hidden-import PySide6.QtCore ^
        --hidden-import PySide6.QtGui ^
        --hidden-import PySide6.QtWidgets ^
        --hidden-import shiboken6 ^
        --hidden-import openpyxl ^
        --hidden-import python_dateutil ^
        --collect-all PySide6 ^
        --exclude-module tkinter ^
        --exclude-module customtkinter ^
        main.py
"""
import sys
import os


def is_frozen() -> bool:
    """Проверить, запущено ли приложение из .exe."""
    return getattr(sys, "frozen", False)


def get_app_dir() -> str:
    """Папка рядом с .exe (для БД, экспортов, пользовательских данных)."""
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_bundle_dir() -> str:
    """Папка с упакованными ресурсами (_MEIPASS для --onefile, или app_dir)."""
    if is_frozen():
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def fix_pyside6_plugins() -> None:
    """Указать Qt плагины для frozen-режима."""
    if not is_frozen():
        return
    base = get_bundle_dir()
    plugin_path = os.path.join(base, "PySide6", "plugins")
    if os.path.isdir(plugin_path):
        os.environ["QT_PLUGIN_PATH"] = plugin_path


def setup_frozen_env() -> None:
    """Настроить окружение для .exe — вызывается из main.py перед GUI."""
    if not is_frozen():
        return
    fix_pyside6_plugins()
    # Гарантируем, что рабочая директория = папка с .exe
    os.chdir(get_app_dir())
