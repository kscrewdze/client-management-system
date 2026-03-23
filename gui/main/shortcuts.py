# -*- coding: utf-8 -*-

"""Горячие клавиши главного окна"""
import customtkinter as ctk


class Shortcuts:
    """Класс для управления горячими клавишами"""
    
    def __init__(self, root, notebook, refresh_callback):
        self.root = root
        self.notebook = notebook
        self.refresh_callback = refresh_callback
    
    def bind_all(self):
        """Привязать все горячие клавиши"""
        self.root.bind('<Control-Key-1>', lambda e: self.notebook.set("📊 Статистика"))
        self.root.bind('<Control-Key-2>', lambda e: self.notebook.set("📋 Клиенты"))
        self.root.bind('<Control-Key-3>', lambda e: self.notebook.set("📊 Матрицы"))
        self.root.bind('<Control-Key-4>', lambda e: self.notebook.set("➕ Добавить"))
        self.root.bind('<Control-Key-5>', lambda e: self.notebook.set("📊 Экспорт"))
        self.root.bind('<Control-Key-6>', lambda e: self.notebook.set("🎨 Темы"))
        self.root.bind('<Control-r>', lambda e: self.refresh_callback())
        self.root.bind('<Control-R>', lambda e: self.refresh_callback())
        self.root.bind('<F5>', lambda e: self.refresh_callback())
        self.root.bind('<F12>', lambda e: self.toggle_debugger()) # F12 для отладчика
        print("✅ Горячие клавиши привязаны")

    def toggle_debugger(self):
        """Переключение отладчика"""
        try:
            from debugger import toggle_debugger
            toggle_debugger()
            print("🔍 Отладчик переключен через горячую клавишу")
        except ImportError as e:
            print(f"❌ Ошибка импорта отладчика: {e}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")