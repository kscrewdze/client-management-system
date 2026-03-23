# -*- coding: utf-8 -*-

"""Действия в диалоге редактирования"""
import customtkinter as ctk
from gui.dialogs.styles import DialogStyles
from utils.validators import Validators
from utils.date_parser import DateParser


class EditActions:
    """Класс для действий в диалоге редактирования"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = parent.dialog
        self.db = parent.db
        self.client = parent.client
        self.client_id = parent.client_id
        self.callback = parent.callback
        self.notifier = parent.notifier
        self.form_widget = parent.form_widget
        self.matrix_widget = parent.matrix_widget
        self.date_widget = parent.date_widget
    
    def create_buttons(self):
        """Создание кнопок с закругленными углами"""
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=10, side="bottom")
        
        # Кнопка Сохранить
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Сохранить",
            command=self.save_client,
            width=120,
            height=35,
            font=("Segoe UI", 11, "bold"),
            fg_color=DialogStyles.COLOR_SUCCESS,
            hover_color="#1e5a23",
            corner_radius=10
        )
        save_btn.pack(side="left", padx=5)
        
        # Кнопка Отмена
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Отмена",
            command=self.parent.destroy,
            width=100,
            height=35,
            font=("Segoe UI", 11, "bold"),
            fg_color=DialogStyles.COLOR_ERROR,
            hover_color="#b71c1c",
            corner_radius=10
        )
        cancel_btn.pack(side="left", padx=5)
    
    def validate_form(self, form_data):
        """Валидация формы"""
        # Имя
        name = form_data.get('name', '')
        is_valid, error = Validators.validate_name(name)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False
        
        # Телефон
        phone = form_data.get('phone', '')
        is_valid, error = Validators.validate_phone(phone)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False
        
        # Telegram
        telegram = form_data.get('telegram', '')
        is_valid, error = Validators.validate_telegram(telegram)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False
        
        # Дата рождения
        birth_str = form_data.get('birth_date', '')
        if not birth_str:
            self.notifier.show_error("❌ Введите дату рождения!")
            return False
        
        is_valid, error, birth_date = Validators.validate_date(birth_str)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False
        
        # Дата заказа
        order_str = form_data.get('order_date', '')
        if not order_str:
            self.notifier.show_error("❌ Введите дату заказа!")
            return False
        
        is_valid, error, order_date = Validators.validate_date(order_str)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False
        
        # Цена
        price_str = form_data.get('price', '')
        if not price_str:
            self.notifier.show_error("❌ Введите цену!")
            return False
        
        is_valid, error, price = Validators.validate_price(price_str)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False
        
        return True
    
    def get_form_data(self):
        """Собрать данные из формы"""
        widgets = self.form_widget.get_all_widgets()
        
        return {
            'name': widgets.get('name').get().strip() if widgets.get('name') else '',
            'telegram': widgets.get('telegram').get().strip() if widgets.get('telegram') else '',
            'phone': widgets.get('phone').get().strip() if widgets.get('phone') else '',
            'birth_date': self.date_widget.birth_entry.get().strip() if self.date_widget.birth_entry else '',
            'order_date': self.date_widget.order_date_entry.get().strip() if self.date_widget.order_date_entry else '',
            'price': self.matrix_widget.price_entry.get().strip() if self.matrix_widget.price_entry else '',
            'comment': widgets.get('comment').get().strip() if widgets.get('comment') else ''
        }
    
    def save_client(self):
        """Сохранение изменений"""
        form_data = self.get_form_data()
        
        if not self.validate_form(form_data):
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
            
            self.db.update_client(self.client_id, client_data)
            
            self.notifier.show_success(f"✅ Данные клиента обновлены!")
            self.parent.destroy()
            self.callback()
            
        except Exception as e:
            self.notifier.show_error(f"❌ Ошибка: {str(e)}")