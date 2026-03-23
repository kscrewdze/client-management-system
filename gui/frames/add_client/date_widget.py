# -*- coding: utf-8 -*-

"""Виджеты для работы с датами"""
from datetime import datetime
import customtkinter as ctk
from widgets.tooltip import ToolTip
from utils.date_parser import DateParser


class DateWidget:
    """Класс для работы с датами"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db  # Получаем db из parent
        self.birth_entry = None
        self.order_date_entry = None
        self.destiny_var = None
        self.destiny_label = None
    
    def create_birth_date_field(self, parent_frame, row):
        """Создание поля для даты рождения"""
        ctk.CTkLabel(
            parent_frame,
            text="📅 Дата рождения:*",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        birth_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        birth_frame.grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.birth_entry = ctk.CTkEntry(
            birth_frame,
            width=120,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="ДД.ММ.ГГГГ"
        )
        self.birth_entry.pack(side="left")
        self.birth_entry.bind('<KeyRelease>', self.update_destiny_number)
        self.birth_entry.bind('<FocusOut>', self.update_destiny_number)  # Добавляем при потере фокуса
        
        ctk.CTkLabel(
            birth_frame,
            text="  Число:",
            font=("Segoe UI", 11),
            text_color="gray"
        ).pack(side="left", padx=(5, 2))
        
        self.destiny_var = ctk.StringVar()
        self.destiny_label = ctk.CTkLabel(
            birth_frame,
            textvariable=self.destiny_var,
            font=("Segoe UI", 12, "bold"),
            text_color="#2b5e8c",
            width=30
        )
        self.destiny_label.pack(side="left")
        
        return self.birth_entry
    
    def create_order_date_field(self, parent_frame, row):
        """Создание поля для даты заказа"""
        ctk.CTkLabel(
            parent_frame,
            text="📅 Дата заказа:*",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        order_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        order_frame.grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.order_date_entry = ctk.CTkEntry(
            order_frame,
            width=120,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="ДД.ММ.ГГГГ"
        )
        self.order_date_entry.pack(side="left")
        self.order_date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        
        today_btn = ctk.CTkButton(
            order_frame,
            text="Сегодня",
            command=self.set_today_date,
            width=70,
            height=28,
            font=("Segoe UI", 10),
            fg_color="#757575",
            hover_color="#616161"
        )
        today_btn.pack(side="left", padx=(5, 0))
        ToolTip(today_btn, "Установить сегодняшнюю дату")
        
        return self.order_date_entry
    
    def set_today_date(self):
        """Установка сегодняшней даты"""
        today = datetime.now().strftime("%d.%m.%Y")
        self.order_date_entry.delete(0, "end")
        self.order_date_entry.insert(0, today)
    
    def update_destiny_number(self, event=None):
        """Обновление числа судьбы"""
        birth_str = self.birth_entry.get().strip()
        if birth_str:
            birth_date = DateParser.parse(birth_str)
            if birth_date and self.db:
                destiny = self.db.calculate_destiny_number(birth_date.strftime("%d.%m.%Y"))
                self.destiny_var.set(str(destiny))
                print(f"🔢 Число судьбы: {destiny} для даты {birth_str}")
            else:
                self.destiny_var.set("?")
                print(f"⚠️ Не удалось распознать дату: {birth_str}")
        else:
            self.destiny_var.set("")
    
    def get_birth_date(self):
        """Получить дату рождения"""
        return self.birth_entry.get().strip()
    
    def get_order_date(self):
        """Получить дату заказа"""
        return self.order_date_entry.get().strip()
    
    def clear(self):
        """Очистить поля с датами"""
        self.birth_entry.delete(0, "end")
        self.order_date_entry.delete(0, "end")
        self.order_date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.destiny_var.set("")