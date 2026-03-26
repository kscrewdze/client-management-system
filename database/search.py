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
        Full-text search across all client fields.

        Searches: name, phone, telegram, comment, service_name,
        matrix name, service_price, birth_date, order_date,
        completed_date, destiny_number.

        Args:
            query: Search string.

        Returns:
            List[Client]: Matching clients.
        """
        try:
            search_term = f"%{query.lower()}%"

            logger.debug("Поиск в БД: '%s'", query)

            with self.db._lock:
                self.db.cursor.execute('''
                    SELECT clients.*, matrices.name as matrix_name
                    FROM clients
                    LEFT JOIN matrices ON clients.matrix_id = matrices.id
                    WHERE UNICODE_LOWER(clients.name) LIKE ?
                       OR UNICODE_LOWER(COALESCE(clients.phone, '')) LIKE ?
                       OR UNICODE_LOWER(COALESCE(clients.telegram, '')) LIKE ?
                       OR UNICODE_LOWER(COALESCE(clients.comment, '')) LIKE ?
                       OR UNICODE_LOWER(COALESCE(clients.service_name, '')) LIKE ?
                       OR UNICODE_LOWER(COALESCE(matrices.name, '')) LIKE ?
                       OR CAST(clients.service_price AS TEXT) LIKE ?
                       OR COALESCE(clients.birth_date, '') LIKE ?
                       OR COALESCE(clients.order_date, '') LIKE ?
                       OR COALESCE(clients.completed_date, '') LIKE ?
                       OR CAST(clients.destiny_number AS TEXT) LIKE ?
                    ORDER BY clients.created_date DESC
                ''', (search_term,) * 11)

                rows = self.db.cursor.fetchall()
            results = [Client.from_db_row(row) for row in rows]

            logger.debug("Найдено: %d клиентов", len(results))
            return results

        except Exception as e:
            logger.error("Ошибка поиска: %s", e)
            return []