#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главный модуль приложения
Версия: 9.0
Автор: kScrewdze
Описание: Современное приложение для управления клиентами и матрицами
"""

import sys
import os
import warnings
import logging
import tkinter as tk
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Глобальный обработчик ошибок Tkinter
def tk_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tk.TclError as e:
            if "invalid command name" in str(e):
                # Игнорируем ошибки after после закрытия
                pass
            else:
                print(f"⚠️ Tkinter ошибка: {e}")
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
    return wrapper


# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ИНИЦИАЛИЗАЦИЯ БУФЕРА ОБМЕНА (до всего остального)
if getattr(sys, 'frozen', False):
    # Мы в .exe
    hidden_root = tk.Tk()
    hidden_root.withdraw()
    from utils.clipboard import init_clipboard
    init_clipboard(hidden_root)
    print("✅ Скрытое окно для буфера обмена создано (exe mode)")
else:
    # Мы в .py
    from utils.clipboard import init_clipboard
    init_clipboard()
    print("✅ Менеджер буфера обмена инициализирован")

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from gui.main import MainApplication


def main():
    """Точка входа в приложение"""
    try:
        logger.info("=" * 50)
        logger.info("ЗАПУСК ПРИЛОЖЕНИЯ")
        logger.info("=" * 50)
        
        app = MainApplication()
        
        logger.info("Приложение успешно инициализировано")
        app.run()
        
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("=" * 50)
        logger.info("ЗАВЕРШЕНИЕ РАБОТЫ")
        logger.info("=" * 50)


if __name__ == "__main__":
    # Применяем декоратор к mainloop
    import tkinter
    tkinter.Tk.mainloop = tk_error_handler(tkinter.Tk.mainloop)
    main()