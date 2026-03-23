# -*- coding: utf-8 -*-

"""Хуки для сборки .exe файла"""
import sys
import os


def fix_clipboard_for_exe():
    """Исправление проблем с буфером обмена в .exe"""
    if getattr(sys, 'frozen', False):
        # Мы в .exe
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        # Держим скрытое окно открытым для доступа к буферу обмена
        return root
    return None


# Добавьте этот код в начало main.py перед созданием приложения
"""
if getattr(sys, 'frozen', False):
    # Мы в .exe, создаем скрытое окно для буфера обмена
    import tkinter as tk
    hidden_root = tk.Tk()
    hidden_root.withdraw()
    from utils.clipboard import init_clipboard
    init_clipboard(hidden_root)
"""