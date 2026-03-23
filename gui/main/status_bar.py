# -*- coding: utf-8 -*-

"""Строка состояния главного окна"""
import os
import customtkinter as ctk
from utils.timer_manager import timer_manager


class StatusBar:
    """Класс для создания строки состояния"""
    
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.status_var = ctk.StringVar()
        self.status_var.set("✅ Готов")
        self.status_frame = None
        self.after_id = None
        self.is_running = True
    
    def create(self):
        """Создание строки состояния"""
        self.status_frame = ctk.CTkFrame(self.parent, height=24, fg_color="#f0f0f0")
        self.status_frame.pack(fill="x", side="bottom")
        self.status_frame.pack_propagate(False)
        
        # Левый статус
        status_label = ctk.CTkLabel(
            self.status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            text_color="#555555"
        )
        status_label.pack(side="left", padx=8)
        
        # Центральный статус с горячими клавишами
        shortcuts_text = "⌨️  Ctrl+1-5: вкладки  |  Ctrl+R: обновить  |  Ctrl+E: ред.  |  Ctrl+D: удал."
        shortcuts_label = ctk.CTkLabel(
            self.status_frame,
            text=shortcuts_text,
            font=("Segoe UI", 9),
            text_color="#555555"
        )
        shortcuts_label.pack(side="left", padx=20, expand=True)
        
        # Правый статус с базой данных
        db_text = f"📁 {os.path.basename(str(self.db_path))}"
        db_label = ctk.CTkLabel(
            self.status_frame,
            text=db_text,
            font=("Segoe UI", 9),
            text_color="#555555"
        )
        db_label.pack(side="right", padx=8)
        
        return self.status_frame
    
    def set_status(self, text):
        """Установить текст статуса"""
        self.status_var.set(text)
    
    def get_status(self):
        """Получить текст статуса"""
        return self.status_var.get()
    
    def cancel_updates(self):
        """Отмена обновлений"""
        self.is_running = False
        if self.after_id:
            try:
                self.status_frame.after_cancel(self.after_id)
                timer_manager.cancel(self.after_id)
                self.after_id = None
            except:
                pass