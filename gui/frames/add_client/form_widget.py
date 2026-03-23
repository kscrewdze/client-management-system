# -*- coding: utf-8 -*-

"""Форма ввода для добавления клиента"""
import customtkinter as ctk


class FormWidget:
    """Класс для создания формы ввода"""
    
    def __init__(self, parent):
        self.parent = parent
        self.widgets = {}
    
    def create_form(self):
        """Создание формы ввода"""
        form_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        form_frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        # Настройка сетки
        form_frame.grid_columnconfigure(0, weight=1, minsize=120)
        form_frame.grid_columnconfigure(1, weight=2)
        
        row = 0
        
        # Имя
        ctk.CTkLabel(
            form_frame,
            text="👤 Имя:*",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        self.widgets['name'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="Иванов Иван"
        )
        self.widgets['name'].grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        row += 1
        
        # Telegram
        ctk.CTkLabel(
            form_frame,
            text="📱 Telegram:",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        self.widgets['telegram'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="@username (необязательно)"
        )
        self.widgets['telegram'].grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        row += 1
        
        # Телефон
        ctk.CTkLabel(
            form_frame,
            text="📞 Телефон:",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        self.widgets['phone'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="+7 (999) 123-45-67 (необязательно)"
        )
        self.widgets['phone'].grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        row += 1
        
        # Дата рождения (будет добавлена отдельно)
        self.birth_row = row
        row += 2  # Пропускаем для date_widget
        
        # Дата заказа (будет добавлена отдельно)
        self.order_row = row
        row += 2  # Пропускаем для date_widget
        
        # Матрица и цена (будут добавлены отдельно)
        self.matrix_row = row
        row += 2  # Пропускаем для matrix_widget
        
        # Комментарий
        ctk.CTkLabel(
            form_frame,
            text="📝 Комментарий:",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        self.widgets['comment'] = ctk.CTkEntry(
            form_frame,
            width=300,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="Дополнительная информация (необязательно)"
        )
        self.widgets['comment'].grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        row += 1
        
        # Примечание
        ctk.CTkLabel(
            form_frame,
            text="* - обязательные поля | Цена заполняется автоматически при выборе матрицы",
            font=("Segoe UI", 9),
            text_color="gray"
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(2, 0))
        
        return form_frame
    
    def get_widget(self, name):
        """Получить виджет по имени"""
        return self.widgets.get(name)
    
    def get_all_widgets(self):
        """Получить все виджеты"""
        return self.widgets
    
    def clear_all(self):
        """Очистить все поля"""
        for widget in self.widgets.values():
            widget.delete(0, "end")