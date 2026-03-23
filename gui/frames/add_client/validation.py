# -*- coding: utf-8 -*-

"""Валидация формы добавления клиента"""
from utils.validators import Validators
from utils.date_parser import DateParser


class FormValidator:
    """Класс для валидации формы"""
    
    def __init__(self, notifier):
        self.notifier = notifier
    
    def validate(self, form_data):
        """
        Валидация всех полей формы
        
        Args:
            form_data: словарь с данными формы
            
        Returns:
            bool: True если валидация пройдена
        """
        # Имя
        name = form_data.get('name', '')
        if not name:
            self.notifier.show_error("❌ Введите имя!")
            return False, 'name'
        
        # Телефон (опционально)
        phone = form_data.get('phone', '')
        is_valid, error = Validators.validate_phone(phone)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False, 'phone'
        
        # Telegram (опционально)
        telegram = form_data.get('telegram', '')
        is_valid, error = Validators.validate_telegram(telegram)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False, 'telegram'
        
        # Дата рождения
        birth_str = form_data.get('birth_date', '')
        if not birth_str:
            self.notifier.show_error("❌ Введите дату рождения!")
            return False, 'birth'
        
        birth_date = DateParser.parse(birth_str)
        if not birth_date:
            self.notifier.show_error("❌ Неверный формат даты рождения!")
            return False, 'birth'
        
        # Дата заказа
        order_str = form_data.get('order_date', '')
        if not order_str:
            self.notifier.show_error("❌ Введите дату заказа!")
            return False, 'order'
        
        order_date = DateParser.parse(order_str)
        if not order_date:
            self.notifier.show_error("❌ Неверный формат даты заказа!")
            return False, 'order'
        
        # Матрица
        selected_matrix = form_data.get('matrix', '')
        if not selected_matrix:
            self.notifier.show_error("❌ Выберите матрицу!")
            return False, 'matrix'
        
        # Цена
        price_str = form_data.get('price', '')
        if not price_str:
            self.notifier.show_error("❌ Введите цену!")
            return False, 'price'
        
        is_valid, error, price = Validators.validate_price(price_str)
        if not is_valid:
            self.notifier.show_error(f"❌ {error}")
            return False, 'price'
        
        return True, None
    
    def get_form_data(self, widgets):
        """Собрать данные из виджетов"""
        return {
            'name': widgets['name'].get().strip(),
            'telegram': widgets['telegram'].get().strip(),
            'phone': widgets['phone'].get().strip(),
            'birth_date': widgets['birth'].get().strip(),
            'order_date': widgets['order'].get().strip(),
            'matrix': widgets['matrix'].get(),
            'price': widgets['price'].get().strip(),
            'comment': widgets['comment'].get().strip()
        }