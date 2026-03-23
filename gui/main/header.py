# -*- coding: utf-8 -*-

"""Заголовок главного окна
Автор: kScrewdze
Версия: 9.0
"""

from datetime import datetime
import customtkinter as ctk
from utils.timer_manager import timer_manager


class Header:
    """Класс для создания заголовка"""
    
    def __init__(self, parent):
        self.parent = parent
        self.datetime_var = ctk.StringVar()
        self.header_frame = None
        self.after_id = None
        self.is_running = True
    
    def create(self, parent_frame):
        """Создание заголовка"""
        self.header_frame = ctk.CTkFrame(parent_frame, height=50, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 5))
        self.header_frame.pack_propagate(False)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            self.header_frame,
            text="🏢 СИСТЕМА УПРАВЛЕНИЯ КЛИЕНТАМИ",
            font=("Segoe UI", 18, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(side="left", padx=8)
        
        # Дата и время
        self.update_datetime()
        
        self.datetime_label = ctk.CTkLabel(
            self.header_frame,
            textvariable=self.datetime_var,
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.datetime_label.pack(side="right", padx=8)
        
        return self.header_frame
    
    def update_datetime(self):
        """Обновление даты и времени"""
        if not self.is_running:
            return
            
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.datetime_var.set(f"📅 {now}")
        
        # Отменяем предыдущий after если есть
        if self.after_id:
            try:
                self.header_frame.after_cancel(self.after_id)
                timer_manager.cancel(self.after_id)
            except:
                pass
            self.after_id = None
        
        # Создаем новый after, только если фрейм существует
        if (hasattr(self, 'header_frame') and 
            self.header_frame and 
            self.header_frame.winfo_exists() and
            self.is_running):
            
            self.after_id = self.header_frame.after(1000, self.update_datetime)
            timer_manager.register(self.after_id)
    
    def cancel_updates(self):
        """Отмена обновлений (вызывается при закрытии)"""
        self.is_running = False
        if self.after_id:
            try:
                self.header_frame.after_cancel(self.after_id)
                timer_manager.cancel(self.after_id)
                self.after_id = None
                print("⏱ Обновление времени остановлено")
            except:
                pass