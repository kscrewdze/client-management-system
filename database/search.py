# -*- coding: utf-8 -*-

"""Поиск клиентов в БД"""
import logging
from typing import List

from database.models import Client

logger = logging.getLogger(__name__)


class SearchDB:
    """Класс для поиска клиентов"""
    
    def __init__(self, db):
        self.db = db
    
    def search_clients(self, query: str) -> List[Client]:
        """
        Поиск клиентов по имени, телефону, telegram или комментарию
        
        Args:
            query: Строка поиска
            
        Returns:
            List[Client]: Список найденных клиентов
        """
        try:
            # Приводим запрос к нижнему регистру для Unicode-совместимого поиска
            search_term = f"%{query.lower()}%"
            
            logger.debug("Поиск в БД: '%s'", query)
            
            # Используем UNICODE_LOWER для case-insensitive поиска кириллицы
            with self.db._lock:
                self.db.cursor.execute('''
                    SELECT clients.*, matrices.name as matrix_name
                    FROM clients 
                    LEFT JOIN matrices ON clients.matrix_id = matrices.id 
                    WHERE UNICODE_LOWER(clients.name) LIKE ? 
                       OR UNICODE_LOWER(clients.phone) LIKE ? 
                       OR UNICODE_LOWER(clients.telegram) LIKE ?
                       OR UNICODE_LOWER(clients.comment) LIKE ?
                    ORDER BY clients.created_date DESC
                ''', (search_term, search_term, search_term, search_term))
                
                rows = self.db.cursor.fetchall()
            results = [Client.from_db_row(row) for row in rows]
            
            logger.debug("Найдено: %d клиентов", len(results))
            return results
            
        except Exception as e:
            logger.error("Ошибка поиска: %s", e)
            return []