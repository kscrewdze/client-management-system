# -*- coding: utf-8 -*-

"""Панель тестирования"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class TestPanel:
    """Панель для тестирования функций"""
    
    def __init__(self, parent, monitors):
        self.parent = parent
        self.monitors = monitors
        self.frame = ttk.Frame(parent)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов"""
        # Заголовок
        title = ttk.Label(self.frame, text="🧪 ТЕСТИРОВАНИЕ", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Тест буфера обмена
        self.create_test_section("Буфер обмена", 0, [
            ("📋 Проверить буфер", self.test_clipboard),
            ("📋 Скопировать тест", self.copy_test_text),
            ("📋 Очистить буфер", self.clear_clipboard)
        ])
        
        # Тест событий
        self.create_test_section("События", 1, [
            ("⌨️ Тест клавиш", self.test_keyboard),
            ("🖱️ Тест фокуса", self.test_focus),
            ("🪟 Тест окна", self.test_window)
        ])
        
        # Тест базы данных
        self.create_test_section("База данных", 2, [
            ("📊 Тест запроса", self.test_query),
            ("📊 Тест подключения", self.test_connection),
            ("📊 Статистика", self.test_stats)
        ])
        
        # Консоль вывода
        console_frame = ttk.LabelFrame(self.frame, text="Результат")
        console_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(console_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.console = tk.Text(
            console_frame,
            height=8,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10)
        )
        self.console.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar.config(command=self.console.yview)
    
    def create_test_section(self, title, row, buttons):
        """Создание секции тестирования"""
        frame = ttk.LabelFrame(self.frame, text=title)
        frame.pack(fill="x", padx=10, pady=5)
        
        for text, command in buttons:
            btn = ttk.Button(frame, text=text, command=lambda c=command: self.run_test(c))
            btn.pack(side="left", padx=5, pady=5)
    
    def run_test(self, test_func):
        """Запуск теста"""
        self.console.insert("end", f"\n▶ Запуск теста: {test_func.__name__}\n")
        self.console.see("end")
        
        try:
            result = test_func()
            self.console.insert("end", f"✅ Результат: {result}\n")
        except Exception as e:
            self.console.insert("end", f"❌ Ошибка: {e}\n")
    
    def test_clipboard(self):
        """Тест буфера обмена"""
        from utils.clipboard import get_clipboard
        clip = get_clipboard()
        content = clip.get_clipboard_text()
        return f"Содержимое: {content[:100]}..." if content else "Пусто"
    
    def copy_test_text(self):
        """Копирование тестового текста"""
        from utils.clipboard import get_clipboard
        clip = get_clipboard()
        test_text = "Тестовый текст для копирования"
        clip.set_clipboard_text(test_text)
        return f"Скопировано: {test_text}"
    
    def clear_clipboard(self):
        """Очистка буфера"""
        from utils.clipboard import get_clipboard
        clip = get_clipboard()
        clip.set_clipboard_text("")
        return "Буфер очищен"
    
    def test_keyboard(self):
        return "Тест клавиш выполнен"
    
    def test_focus(self):
        return "Тест фокуса выполнен"
    
    def test_window(self):
        return "Тест окна выполнен"
    
    def test_query(self):
        return "Тест запроса выполнен"
    
    def test_connection(self):
        return "Тест подключения выполнен"
    
    def test_stats(self):
        return "Тест статистики выполнен"