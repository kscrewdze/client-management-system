# -*- coding: utf-8 -*-

"""Виджеты для работы с датами в редактировании"""
from datetime import datetime
import customtkinter as ctk
from gui.dialogs.styles import DialogStyles
from utils.date_parser import DateParser


class EditDateWidget:
    """Класс для работы с датами в редактировании"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = parent.dialog
        self.client = parent.client
        self.db = parent.db
        self.birth_entry = None
        self.order_date_entry = None
        self.destiny_var = None
    
    def create_birth_date_field(self, form_frame, row):
        """Создание поля для даты рождения"""
        ctk.CTkLabel(
            form_frame,
            text="📅 Дата рождения:*",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        birth_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        birth_frame.grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.birth_entry = ctk.CTkEntry(
            birth_frame,
            width=120,
            height=30,
            font=DialogStyles.FONT_NORMAL
        )
        self.birth_entry.pack(side="left")
        self.birth_entry.insert(0, self.client.birth_date)
        self.birth_entry.bind('<KeyRelease>', self.update_destiny_number)
        self.parent.bind_paste_shortcut(self.birth_entry)
        
        ctk.CTkLabel(
            birth_frame,
            text="  Число:",
            font=DialogStyles.FONT_NORMAL,
            text_color="gray"
        ).pack(side="left", padx=(5, 2))
        
        self.destiny_var = ctk.StringVar()
        self.destiny_var.set(str(self.client.destiny_number))
        
        self.destiny_label = ctk.CTkLabel(
            birth_frame,
            textvariable=self.destiny_var,
            font=("Segoe UI", 12, "bold"),
            text_color=DialogStyles.COLOR_PRIMARY,
            width=30
        )
        self.destiny_label.pack(side="left")
        
        return self.birth_entry
    
    def create_order_date_field(self, form_frame, row):
        """Создание поля для даты заказа"""
        ctk.CTkLabel(
            form_frame,
            text="📅 Дата заказа:*",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        order_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        order_frame.grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.order_date_entry = ctk.CTkEntry(
            order_frame,
            width=120,
            height=30,
            font=DialogStyles.FONT_NORMAL
        )
        self.order_date_entry.pack(side="left")
        self.order_date_entry.insert(0, self.client.order_date)
        self.parent.bind_paste_shortcut(self.order_date_entry)
        
        today_btn = ctk.CTkButton(
            order_frame,
            text="Сегодня",
            command=self.set_today_date,
            width=70,
            height=28,
            font=DialogStyles.FONT_SMALL,
            fg_color=DialogStyles.COLOR_GRAY,
            hover_color="#616161"
        )
        today_btn.pack(side="left", padx=(5, 0))
        
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
            if birth_date:
                destiny = self.db.calculate_destiny_number(birth_date.strftime("%d.%m.%Y"))
                self.destiny_var.set(str(destiny))
            else:
                self.destiny_var.set("?")