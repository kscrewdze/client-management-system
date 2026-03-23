# -*- coding: utf-8 -*-

"""Статистика по БД"""
from typing import Dict, Any


class StatisticsDB:
    """Класс для получения статистики"""
    
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor
        self.conn = db.conn
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики"""
        self.cursor.execute('SELECT COUNT(*), SUM(service_price) FROM clients')
        total_count, total_sum = self.cursor.fetchone()
        
        self.cursor.execute('SELECT COUNT(*), SUM(service_price) FROM clients WHERE is_completed = 1')
        completed_count, completed_sum = self.cursor.fetchone()
        
        self.cursor.execute('SELECT AVG(service_price) FROM clients')
        avg_price = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM matrices')
        matrices_count = self.cursor.fetchone()[0]
        
        stats = {
            'total_clients': total_count or 0,
            'total_earnings': total_sum or 0,
            'completed_count': completed_count or 0,
            'completed_earnings': completed_sum or 0,
            'average_price': avg_price or 0,
            'matrices_count': matrices_count or 0
        }
        
        print(f"📊 Статистика: {stats}")
        return stats