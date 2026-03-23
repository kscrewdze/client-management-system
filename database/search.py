# -*- coding: utf-8 -*-

"""Поиск клиентов в БД"""
from typing import List

from database.models import Client


class SearchDB:
    """Класс для поиска клиентов"""
    
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor
        self.conn = db.conn
    
    def search_clients(self, query: str) -> List[Client]:
        """
        Поиск клиентов по имени, телефону, telegram или комментарию
        
        Args:
            query: Строка поиска
            
        Returns:
            List[Client]: Список найденных клиентов
        """
        try:
            # Проверяем соединение
            if not self.conn:
                self.db.connect()
            
            # Подготавливаем поисковый запрос
            search_term = f"%{query}%"
            
            print(f"\n🔍 ПОИСК В БД:")
            print(f"   Запрос: '{query}'")
            
            # Выполняем поиск
            self.cursor.execute('''
                SELECT clients.*, matrices.name as matrix_name
                FROM clients 
                LEFT JOIN matrices ON clients.matrix_id = matrices.id 
                WHERE clients.name LIKE ? 
                   OR clients.phone LIKE ? 
                   OR clients.telegram LIKE ?
                   OR clients.comment LIKE ?
                ORDER BY clients.created_date DESC
            ''', (search_term, search_term, search_term, search_term))
            
            rows = self.cursor.fetchall()
            results = [Client.from_db_row(row) for row in rows]
            
            print(f"   Найдено: {len(results)} клиентов")
            return results
            
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")
            return []