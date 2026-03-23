# -*- coding: utf-8 -*-

"""Форма редактирования клиента"""
import customtkinter as ctk
from gui.dialogs.styles import DialogStyles


class EditFormWidget:
    """Класс для создания формы редактирования"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = parent.dialog
        self.client = parent.client
        self.db = parent.db
        self.widgets = {}
    
    def create_form(self, container):
        """Создание формы"""
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Настройка сетки
        form_frame.grid_columnconfigure(0, weight=1, minsize=100)
        form_frame.grid_columnconfigure(1, weight=3)
        
        row = 0
        
        # Имя
        ctk.CTkLabel(
            form_frame,
            text="👤 Имя:*",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=3)
        
        self.widgets['name'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=28,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="Иванов Иван",
            corner_radius=8
        )
        self.widgets['name'].grid(row=row, column=1, sticky="w", pady=3, padx=(5, 0))
        self.widgets['name'].insert(0, self.client.name)
        row += 1
        
        # Telegram
        ctk.CTkLabel(
            form_frame,
            text="📱 Telegram:",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=3)
        
        self.widgets['telegram'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=28,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="@username (необязательно)",
            corner_radius=8
        )
        self.widgets['telegram'].grid(row=row, column=1, sticky="w", pady=3, padx=(5, 0))
        if self.client.telegram:
            self.widgets['telegram'].insert(0, self.client.telegram)
        row += 1
        
        # Телефон
        ctk.CTkLabel(
            form_frame,
            text="📞 Телефон:",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=3)
        
        self.widgets['phone'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=28,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="+7 (999) 123-45-67 (необязательно)",
            corner_radius=8
        )
        self.widgets['phone'].grid(row=row, column=1, sticky="w", pady=3, padx=(5, 0))
        if self.client.phone:
            self.widgets['phone'].insert(0, self.client.phone)
        row += 1
        
        # Дата рождения (будет добавлена из date_widget)
        self.birth_row = row
        row += 2
        
        # Дата заказа (будет добавлена из date_widget)
        self.order_row = row
        row += 2
        
        # Матрица (будет добавлена из matrix_widget)
        self.matrix_row = row
        row += 2
        
        # Цена (будет добавлена из matrix_widget)
        self.price_row = row
        row += 2
        
        # Комментарий
        ctk.CTkLabel(
            form_frame,
            text="📝 Комментарий:",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=3)
        
        self.widgets['comment'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=28,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="Дополнительная информация (необязательно)",
            corner_radius=8
        )
        self.widgets['comment'].grid(row=row, column=1, sticky="w", pady=3, padx=(5, 0))
        if self.client.comment:
            self.widgets['comment'].insert(0, self.client.comment)
        row += 1
        
        return form_frame
    
    def get_widget(self, name):
        """Получить виджет по имени"""
        return self.widgets.get(name)
    
    def get_all_widgets(self):
        """Получить все виджеты"""
        return self.widgets