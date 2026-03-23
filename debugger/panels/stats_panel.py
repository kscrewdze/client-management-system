# -*- coding: utf-8 -*-

"""Панель статистики"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class StatsPanel:
    """Панель статистики"""
    
    def __init__(self, parent, monitors):
        self.parent = parent
        self.monitors = monitors
        self.frame = ttk.Frame(parent)
        self.labels = {}
        
        self.create_widgets()
        self.update_stats()
    
    def create_widgets(self):
        """Создание виджетов"""
        # Заголовок
        title = ttk.Label(self.frame, text="📊 СТАТИСТИКА РАБОТЫ", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Статистика буфера обмена
        self.create_stats_section("Буфер обмена", 0, [
            "Проверок",
            "Вставок",
            "Последнее содержимое"
        ])
        
        # Статистика событий
        self.create_stats_section("События", 1, [
            "Всего событий",
            "Последние события"
        ])
        
        # Статистика горячих клавиш
        self.create_stats_section("Горячие клавиши", 2, [
            "Зарегистрировано",
            "Использовано"
        ])
        
        # Статистика базы данных
        self.create_stats_section("База данных", 3, [
            "Запросов",
            "Последние запросы"
        ])
        
        # Кнопка обновления
        ttk.Button(self.frame, text="🔄 Обновить", command=self.update_stats).pack(pady=10)
    
    def create_stats_section(self, title, row, fields):
        """Создание секции статистики"""
        frame = ttk.LabelFrame(self.frame, text=title)
        frame.pack(fill="x", padx=10, pady=5)
        
        for i, field in enumerate(fields):
            label = ttk.Label(frame, text=f"{field}:")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            value = ttk.Label(frame, text="...")
            value.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            
            self.labels[f"{title}_{field}"] = value
    
    def update_stats(self):
        """Обновление статистики"""
        # Статистика буфера обмена
        if 'clipboard' in self.monitors:
            stats = self.monitors['clipboard'].get_stats()
            self.labels['Буфер обмена_Проверок'].config(text=str(stats['checks']))
            self.labels['Буфер обмена_Вставок'].config(text=str(stats['pastes']))
            self.labels['Буфер обмена_Последнее содержимое'].config(
                text=stats['last_content'][:50] + "..." if stats['last_content'] else "Нет"
            )
        
        # Статистика событий
        if 'event' in self.monitors:
            stats = self.monitors['event'].get_stats()
            self.labels['События_Всего событий'].config(text=str(stats['total_events']))
            self.labels['События_Последние события'].config(
                text=str(len(stats['recent_events']))
            )
        
        # Статистика горячих клавиш
        if 'shortcut' in self.monitors:
            stats = self.monitors['shortcut'].get_stats()
            self.labels['Горячие клавиши_Зарегистрировано'].config(text=str(stats['registered']))
            self.labels['Горячие клавиши_Использовано'].config(text=str(stats['used']))
        
        # Статистика базы данных
        if 'database' in self.monitors:
            stats = self.monitors['database'].get_stats()
            self.labels['База данных_Запросов'].config(text=str(stats['total_queries']))
            self.labels['База данных_Последние запросы'].config(
                text=str(len(stats['recent_queries']))
            )
        
        # Обновление каждые 2 секунды
        self.frame.after(2000, self.update_stats)