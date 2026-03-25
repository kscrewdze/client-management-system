# -*- coding: utf-8 -*-

"""Подсветка текста в результатах поиска"""
import logging
import re
from typing import List
from database.models import Client


class TextHighlighter:
    """Класс для подсветки текста"""
    
    @staticmethod
    def highlight(text: str, query: str) -> str:
        """
        Подсветка найденного текста
        
        Args:
            text: исходный текст
            query: поисковый запрос
            
        Returns:
            str: текст с маркерами подсветки
        """
        if not query or not text or len(query) < 2:
            return text
        
        try:
            # Экранируем спецсимволы
            clean_query = re.escape(query)
            # Создаем регулярное выражение (регистронезависимое)
            pattern = re.compile(f'({clean_query})', re.IGNORECASE)
            # Заменяем на подсвеченный вариант
            highlighted = pattern.sub(r'[\1]', text)
            return highlighted
        except (re.error, TypeError) as e:
            logging.getLogger(__name__).debug("Ошибка подсветки: %s", e)
            return text
    
    @staticmethod
    def highlight_client_fields(client: Client, query: str) -> dict:
        """
        Подсветка полей клиента
        
        Args:
            client: объект клиента
            query: поисковый запрос
            
        Returns:
            dict: словарь с подсвеченными полями
        """
        result = {}
        
        # Подсвечиваем имя
        result['name'] = TextHighlighter.highlight(client.name, query)
        
        # Подсвечиваем телефон
        if client.phone:
            result['phone'] = TextHighlighter.highlight(client.phone, query)
        else:
            result['phone'] = client.phone
        
        # Подсвечиваем Telegram
        if client.telegram:
            result['telegram'] = TextHighlighter.highlight(client.telegram, query)
        else:
            result['telegram'] = client.telegram
        
        # Подсвечиваем комментарий
        if client.comment:
            result['comment'] = TextHighlighter.highlight(client.comment, query)
        else:
            result['comment'] = client.comment
        
        return result
    
    @staticmethod
    def highlight_in_list(clients: List[Client], query: str) -> List[dict]:
        """
        Подсветка полей для списка клиентов
        
        Args:
            clients: список клиентов
            query: поисковый запрос
            
        Returns:
            List[dict]: список словарей с подсвеченными полями
        """
        result = []
        for client in clients:
            highlighted = TextHighlighter.highlight_client_fields(client, query)
            highlighted['id'] = client.id
            highlighted['matrix'] = client.matrix_name
            highlighted['price'] = client.service_price
            highlighted['order_date'] = client.order_date
            highlighted['birth_date'] = client.birth_date
            highlighted['destiny'] = client.destiny_number
            highlighted['completed'] = client.is_completed
            result.append(highlighted)
        
        return result


# Создаем глобальный экземпляр
highlighter = TextHighlighter()