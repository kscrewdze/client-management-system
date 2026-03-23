# -*- coding: utf-8 -*-

"""Парсер даты"""
from datetime import datetime
from typing import Optional
import re

from config.settings import Settings


class DateParser:
    """Класс для парсинга даты в разных форматах"""
    
    @classmethod
    def parse(cls, date_str: str) -> Optional[datetime]:
        """Парсинг строки даты"""
        if not date_str or not isinstance(date_str, str):
            return None
        
        date_str = date_str.strip()
        if not date_str:
            return None
        
        # Удаляем все разделители для проверки
        clean_str = re.sub(r'[.\-/]', '', date_str)
        
        # Пробуем стандартные форматы
        for fmt in Settings.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Пробуем формат ДДММГГГГ
        if len(clean_str) == 8 and clean_str.isdigit():
            try:
                day = int(clean_str[0:2])
                month = int(clean_str[2:4])
                year = int(clean_str[4:8])
                return datetime(year, month, day)
            except ValueError:
                pass
        
        # Пробуем формат ГГГГММДД
        if len(clean_str) == 8 and clean_str.isdigit():
            try:
                year = int(clean_str[0:4])
                month = int(clean_str[4:6])
                day = int(clean_str[6:8])
                return datetime(year, month, day)
            except ValueError:
                pass
        
        return None
    
    @classmethod
    def format_date(cls, date: datetime, format: str = "%d.%m.%Y") -> str:
        """Форматирование даты"""
        return date.strftime(format)
    
    @classmethod
    def get_month_name(cls, month_number: int) -> str:
        """Получение названия месяца по номеру"""
        months = {
            1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
            5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
            9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
        }
        return months.get(month_number, f"Месяц {month_number}")