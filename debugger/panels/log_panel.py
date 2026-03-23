# -*- coding: utf-8 -*-

"""Панель логов отладчика"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime


class LogPanel:
    """Панель отображения логов"""
    
    def __init__(self, parent, message_queue):
        self.parent = parent
        self.message_queue = message_queue
        self.frame = ttk.Frame(parent)
        self.logs = []
        self.filter_var = tk.StringVar()
        self.filter_var.trace('w', self.apply_filter)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов"""
        # Панель инструментов
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(toolbar, text="Фильтр:").pack(side="left", padx=(0,5))
        
        filter_entry = ttk.Entry(toolbar, textvariable=self.filter_var, width=20)
        filter_entry.pack(side="left", padx=5)
        
        ttk.Button(toolbar, text="Применить", command=self.apply_filter).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Очистить", command=self.clear_filter).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Очистить логи", command=self.clear).pack(side="right", padx=5)
        
        # Текстовое поле с прокруткой
        text_frame = ttk.Frame(self.frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.text_widget = tk.Text(
            text_frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            wrap="word",
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.text_widget.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=self.text_widget.yview)
        
        # Настройка тегов для цветов
        self.text_widget.tag_config("INFO", foreground="#4ec9b0")
        self.text_widget.tag_config("ERROR", foreground="#f48771")
        self.text_widget.tag_config("WARNING", foreground="#dcdcaa")
        self.text_widget.tag_config("CLIPBOARD", foreground="#ce9178")
        self.text_widget.tag_config("SHORTCUT", foreground="#c586c0")
        self.text_widget.tag_config("EVENT", foreground="#9cdcfe")
        self.text_widget.tag_config("DATABASE", foreground="#6a9955")
        self.text_widget.tag_config("TIME", foreground="#808080")
    
    def add_message(self, msg):
        """Добавление сообщения"""
        self.logs.append(msg)
        
        # Проверяем фильтр
        filter_text = self.filter_var.get().lower()
        if filter_text and filter_text not in msg['message'].lower():
            return
        
        # Форматирование времени
        time_str = msg['time'].strftime("%H:%M:%S.%f")[:-3]
        
        # Вставка в текстовое поле
        self.text_widget.insert("end", f"[{time_str}] ", "TIME")
        
        level = msg.get('level', 'INFO')
        self.text_widget.insert("end", f"[{level}] ", level)
        
        self.text_widget.insert("end", f"{msg['message']}\n")
        self.text_widget.see("end")
    
    def apply_filter(self, *args):
        """Применить фильтр"""
        self.text_widget.delete("1.0", "end")
        filter_text = self.filter_var.get().lower()
        
        for msg in self.logs:
            if not filter_text or filter_text in msg['message'].lower():
                time_str = msg['time'].strftime("%H:%M:%S.%f")[:-3]
                level = msg.get('level', 'INFO')
                
                self.text_widget.insert("end", f"[{time_str}] ", "TIME")
                self.text_widget.insert("end", f"[{level}] ", level)
                self.text_widget.insert("end", f"{msg['message']}\n")
        
        self.text_widget.see("end")
    
    def clear_filter(self):
        """Очистить фильтр"""
        self.filter_var.set("")
        self.apply_filter()
    
    def clear(self):
        """Очистить все логи"""
        self.logs.clear()
        self.text_widget.delete("1.0", "end")
    
    def get_all(self):
        """Получить все логи"""
        return self.logs.copy()