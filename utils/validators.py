# -*- coding: utf-8 -*-

"""Валидаторы данных"""
import re
from typing import Tuple, Optional, Any
from datetime import datetime


class Validators:
    """Класс с методами валидации"""
    
    @staticmethod
    def validate_name(name: Any) -> Tuple[bool, str]:
        """Валидация имени"""
        if not name:
            return False, "Имя не может быть пустым"
        
        if not isinstance(name, str):
            return False, "Имя должно быть строкой"
        
        name = name.strip()
        if not name:
            return False, "Имя не может быть пустым"
        
        if len(name) < 2:
            return False, "Имя должно содержать минимум 2 символа"
        
        if len(name) > 100:
            return False, "Имя слишком длинное (макс. 100 символов)"
        
        # Проверка на недопустимые символы
        if re.search(r'[<>{}[\]\\]', name):
            return False, "Имя содержит недопустимые символы"
        
        return True, ""
    
    @staticmethod
    def validate_phone(phone: Any) -> Tuple[bool, str]:
        """Валидация телефона"""
        if not phone:
            return True, ""  # Телефон не обязателен
        
        if not isinstance(phone, str):
            phone = str(phone)
        
        # Удаляем все нецифровые символы
        clean_phone = re.sub(r'\D', '', phone)
        
        if not clean_phone:
            return True, ""  # Пустой после очистки - считаем валидным
        
        if len(clean_phone) < 10:
            return False, "Телефон должен содержать минимум 10 цифр"
        
        if len(clean_phone) > 15:
            return False, "Телефон слишком длинный (макс. 15 цифр)"
        
        return True, ""
    
    @staticmethod
    def validate_price(price_str: Any) -> Tuple[bool, str, Optional[float]]:
        """Валидация цены"""
        if not price_str:
            return False, "Цена не может быть пустой", None
        
        if isinstance(price_str, (int, float)):
            price = float(price_str)
        else:
            try:
                price = float(str(price_str).replace(',', '.').strip())
            except (ValueError, TypeError):
                return False, "Цена должна быть числом", None
        
        if price < 0:
            return False, "Цена не может быть отрицательной", None
        
        if price > 10_000_000:
            return False, "Цена слишком большая (макс. 10 млн.)", None
        
        return True, "", price
    
    @staticmethod
    def validate_telegram(telegram: Any) -> Tuple[bool, str]:
        """Валидация Telegram username"""
        if not telegram:
            return True, ""
        
        if not isinstance(telegram, str):
            telegram = str(telegram)
        
        telegram = telegram.strip()
        if telegram.startswith('@'):
            telegram = telegram[1:]
        
        if not telegram:
            return True, ""
        
        # Telegram username может содержать буквы, цифры и подчеркивание
        if not re.match(r'^[a-zA-Z0-9_]{5,32}$', telegram):
            return False, "Telegram username должен содержать 5-32 символов: буквы, цифры, _"
        
        return True, ""
    
    @staticmethod
    def validate_date(date_str: Any) -> Tuple[bool, str, Optional[datetime]]:
        """Валидация даты"""
        if not date_str:
            return False, "Дата не может быть пустой", None
        
        if not isinstance(date_str, str):
            date_str = str(date_str)
        
        from utils.date_parser import DateParser
        date = DateParser.parse(date_str)
        
        if not date:
            return False, "Неверный формат даты. Используйте ДД.ММ.ГГГГ", None
        
        # Проверка на разумные пределы дат
        current_year = datetime.now().year
        if date.year < 1900 or date.year > current_year + 1:
            return False, f"Год должен быть между 1900 и {current_year + 1}", None
        
        return True, "", date