# -*- coding: utf-8 -*-

"""Управление историей поиска"""
from typing import List
import logging

logger = logging.getLogger(__name__)


class SearchHistory:
    """Класс для управления историей поиска"""
    
    def __init__(self, max_history: int = 5):
        """
        Инициализация истории поиска
        
        Args:
            max_history: максимальный размер истории
        """
        self.history: List[str] = []
        self.max_history = max_history
        logger.debug("SearchHistory инициализирован")
    
    def add(self, query: str) -> bool:
        """
        Добавить запрос в историю
        
        Args:
            query: поисковый запрос
            
        Returns:
            bool: True если добавлен, False если нет
        """
        if not query or len(query.strip()) < 4:
            return False
        
        clean_query = query.strip().lower()
        
        # Проверяем, что это не расширение предыдущего запроса
        if self.history:
            last = self.history[-1]
            if clean_query.startswith(last) and len(clean_query) == len(last) + 1:
                logger.debug("Расширение '%s', не добавляем в историю", last)
                return False
        
        # Добавляем только новый запрос
        if not self.history or self.history[-1] != clean_query:
            self.history.append(clean_query)
            # Ограничиваем историю
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            logger.debug("Добавлено в историю: %s", clean_query)
            return True
        
        return False
    
    def get_all(self) -> List[str]:
        """Получить всю историю"""
        return self.history.copy()
    
    def get_last(self) -> str:
        """Получить последний запрос"""
        return self.history[-1] if self.history else ""
    
    def clear(self):
        """Очистить историю"""
        self.history.clear()
        logger.debug("История поиска очищена")
    
    def remove(self, query: str) -> bool:
        """Удалить конкретный запрос из истории"""
        if query in self.history:
            self.history.remove(query)
            return True
        return False


# Создаем глобальный экземпляр
history_manager = SearchHistory()


def get_history() -> SearchHistory:
    """Получить глобальный менеджер истории"""
    return history_manager