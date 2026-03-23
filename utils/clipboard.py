# -*- coding: utf-8 -*-

"""Утилиты для работы с буфером обмена"""
import tkinter as tk
import logging
import sys

logger = logging.getLogger(__name__)


class ClipboardManager:
    """Менеджер для работы с буфером обмена"""
    
    def __init__(self, root_window=None):
        self.root = root_window
        self.debug_mode = True
        self.hidden_root = None
        self._create_hidden_window()
        print("✅ ClipboardManager инициализирован")
    
    def _create_hidden_window(self):
        """Создать скрытое окно для доступа к буферу обмена"""
        try:
            if not self.root:
                self.hidden_root = tk.Tk()
                self.hidden_root.withdraw()
                print("   Скрытое окно для буфера обмена создано")
            else:
                print("   Используется главное окно для буфера обмена")
        except Exception as e:
            print(f"   Ошибка создания окна: {e}")
    
    def get_clipboard_text(self) -> str:
        """Получить текст из буфера обмена"""
        # Пробуем разные способы получения текста
        methods = []
        
        # Способ 1: через главное окно
        if self.root:
            methods.append(("главное окно", self.root))
        
        # Способ 2: через скрытое окно
        if self.hidden_root:
            methods.append(("скрытое окно", self.hidden_root))
        
        for method_name, window in methods:
            try:
                text = window.clipboard_get()
                if text:
                    print(f"📋 Получен текст через {method_name}: {len(text)} символов")
                    return text
            except tk.TclError:
                # Буфер обмена пуст - это нормально
                pass
            except Exception as e:
                print(f"⚠️ Ошибка через {method_name}: {e}")
        
        # Способ 3: временное окно
        try:
            temp_root = tk.Tk()
            temp_root.withdraw()
            text = temp_root.clipboard_get()
            temp_root.destroy()
            if text:
                print(f"📋 Получен текст через временное окно: {len(text)} символов")
                return text
        except:
            pass
        
        return ""
    
    def set_clipboard_text(self, text: str) -> bool:
        """Установить текст в буфер обмена"""
        try:
            if self.root:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.root.update()
                print(f"📋 Текст скопирован в буфер: {len(text)} символов")
                return True
        except Exception as e:
            print(f"❌ Ошибка копирования: {e}")
        return False


# Глобальный экземпляр
clipboard_manager = None


def init_clipboard(root_window=None):
    """Инициализация глобального менеджера буфера обмена"""
    global clipboard_manager
    clipboard_manager = ClipboardManager(root_window)
    return clipboard_manager


def get_clipboard():
    """Получить глобальный менеджер буфера обмена"""
    global clipboard_manager
    if clipboard_manager is None:
        clipboard_manager = ClipboardManager()
    return clipboard_manager