# -*- coding: utf-8 -*-

"""Базовый фрейм для добавления клиента"""
from datetime import datetime
import customtkinter as ctk

from database import Database
from widgets.notifications import NotificationLabel
from widgets.tooltip import ToolTip
from utils.date_parser import DateParser

from gui.frames.add_client.form_widget import FormWidget
from gui.frames.add_client.date_widget import DateWidget
from gui.frames.add_client.matrix_widget import MatrixWidget
from gui.frames.add_client.validation import FormValidator
from gui.frames.add_client.shortcuts import ShortcutManager


class AddClientFrame(ctk.CTkFrame):
    """Фрейм для добавления нового клиента"""
    
    def __init__(self, parent, db: Database, callback, notifier: NotificationLabel):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.callback = callback
        self.notifier = notifier
        self.name_entry = None
        self.price_entry = None
    
        # Инициализируем компоненты
        self.form_widget = FormWidget(self)
        self.date_widget = DateWidget(self)  # db будет доступен через self
        self.matrix_widget = MatrixWidget(self, notifier)
        self.validator = FormValidator(notifier)
        self.shortcuts = ShortcutManager(self, notifier)
    
    def create_widgets(self):
        """Создание виджетов"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="➕ ДОБАВЛЕНИЕ КЛИЕНТА",
            font=("Segoe UI", 16, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(pady=(5, 2))
        
        # Подсказка
        hint_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", height=24)
        hint_frame.pack(fill="x", padx=15, pady=(0, 5))
        hint_frame.pack_propagate(False)
        
        hint_label = ctk.CTkLabel(
            hint_frame,
            text="💡 Ctrl+Enter - сохранить | Ctrl+Q - очистить | Ctrl+V - вставить",
            font=("Segoe UI", 10),
            text_color="#666666"
        )
        hint_label.pack(expand=True)
        
        # Создаем форму
        form_frame = self.form_widget.create_form()
        
        # Получаем виджеты из формы
        widgets = self.form_widget.get_all_widgets()
        
        # Сохраняем name_entry для доступа из других методов
        self.name_entry = widgets.get('name')
        
        # Дата рождения
        birth_entry = self.date_widget.create_birth_date_field(form_frame, self.form_widget.birth_row)
        birth_entry.bind('<KeyRelease>', lambda e: self.date_widget.update_destiny_number(e, self.db))
        widgets['birth'] = birth_entry
        
        # Дата заказа
        order_entry = self.date_widget.create_order_date_field(form_frame, self.form_widget.order_row)
        widgets['order'] = order_entry
        
        # Матрица и цена
        matrix_combo, price_entry = self.matrix_widget.create_matrix_field(form_frame, self.form_widget.matrix_row)
        widgets['matrix'] = matrix_combo
        widgets['price'] = price_entry
        self.price_entry = price_entry
        
        # Кнопки (СОЗДАЕМ ПОСЛЕ ТОГО КАК name_entry УЖЕ ЕСТЬ)
        self.create_buttons()
    
    def create_buttons(self):
        """Создание кнопок"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=8)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Сохранить (Ctrl+Enter)",
            command=self.save_client,
            width=150,
            height=32,
            font=("Segoe UI", 11, "bold"),
            fg_color="#2e7d32",
            hover_color="#1e5a23"
        )
        save_btn.pack(side="left", padx=3)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Очистить (Ctrl+Q)",
            command=self.clear_form,
            width=130,
            height=32,
            font=("Segoe UI", 11, "bold"),
            fg_color="#ed6c02",
            hover_color="#db6a00"
        )
        clear_btn.pack(side="left", padx=3)
        
        # Устанавливаем фокус на поле имени
        if self.name_entry:
            self.name_entry.focus()
    
    def load_matrices(self):
        """Загрузка списка матриц"""
        self.matrix_widget.load_matrices(self.db)
    
    def bind_shortcuts(self):
        widgets = self.form_widget.get_all_widgets()
        entries = list(widgets.values())
    
        print(f"\n🔧 Найденные поля для привязки:")
        for i, entry in enumerate(entries):
            print(f"  Поле {i+1}: {entry}")
    
        self.shortcuts.bind_paste_to_entries(entries)
        self.shortcuts.bind_save_shortcut(entries, self.save_client)
        self.shortcuts.bind_clear_shortcut(entries, self.clear_form)
    
        # Тестирование
        self.shortcuts.test_shortcuts(entries)
    
        print("✅ Все горячие клавиши привязаны")
    
    def save_client(self):
        """Сохранение клиента"""
        widgets = self.form_widget.get_all_widgets()
        form_data = self.validator.get_form_data(widgets)
        
        # Валидация
        is_valid, error_field = self.validator.validate(form_data)
        if not is_valid:
            return
        
        try:
            name = form_data['name']
            telegram = form_data['telegram'] or None
            phone = form_data['phone'] or None
            birth_str = form_data['birth_date']
            order_str = form_data['order_date']
            price_str = form_data['price']
            comment = form_data['comment'] or None
            
            birth_date = DateParser.parse(birth_str)
            order_date = DateParser.parse(order_str)
            
            matrix_name, matrix_id = self.matrix_widget.get_matrix_info()
            
            destiny_number = self.db.calculate_destiny_number(birth_date.strftime("%d.%m.%Y"))
            
            client_data = {
                'name': name,
                'telegram': telegram,
                'phone': phone,
                'birth_date': birth_date.strftime("%d.%m.%Y"),
                'order_date': order_date.strftime("%d.%m.%Y"),
                'service_name': matrix_name,
                'service_price': float(price_str.replace(',', '.')),
                'comment': comment,
                'matrix_id': matrix_id,
                'destiny_number': destiny_number
            }
            
            self.db.add_client(client_data)
            
            self.notifier.show_success(f"✅ Клиент {name} добавлен!")
            self.clear_form()
            self.callback()
            
            try:
                self.master.master.set("📋 Клиенты")
            except:
                pass
            
        except Exception as e:
            self.notifier.show_error(f"❌ Ошибка: {str(e)}")
    
    def clear_form(self):
        """Очистка формы"""
        self.form_widget.clear_all()
        self.date_widget.clear()
        self.matrix_widget.clear()
        if self.name_entry:
            self.name_entry.focus()