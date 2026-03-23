# -*- coding: utf-8 -*-

"""Вспомогательные методы для работы с БД"""
import re


def calculate_destiny_number(birth_date: str) -> int:
    """Расчет числа судьбы из даты рождения"""
    # Удаляем все разделители
    date_str = re.sub(r'[.\-/]', '', birth_date)
    
    # Проверяем, что строка содержит только цифры
    if not date_str or not date_str.isdigit():
        return 0
    
    digits = [int(d) for d in date_str]
    total = sum(digits)
    
    # Сводим к числу от 1 до 22
    while total > 22:
        total = sum(int(d) for d in str(total))
    
    return total