# -*- coding: utf-8 -*-

"""Мониторинг базы данных"""
import threading
from datetime import datetime


class DatabaseMonitor(threading.Thread):
    """Монитор базы данных"""
    
    def __init__(self, message_queue):
        super().__init__(daemon=True)
        self.message_queue = message_queue
        self.running = True
        self.queries = []
        self.query_count = 0
        self.db = None
    
    def run(self):
        """Запуск мониторинга"""
        self._log("🔄 Мониторинг базы данных запущен")
        while self.running:
            threading.Event().wait(1.0)
    
    def _log(self, message):
        """Внутренний метод для логирования"""
        try:
            self.message_queue.put({
                'time': datetime.now(),
                'level': 'DATABASE',
                'message': message,
                'source': 'database'
            })
        except:
            pass
    
    def set_db(self, db):
        """Установка ссылки на БД"""
        self.db = db
        self._log("📊 Подключен к базе данных")
    
    def log_query(self, query, params=None, result=None):
        """Логирование запроса к БД"""
        self.query_count += 1
        query_info = {
            'time': datetime.now(),
            'query': query,
            'params': params,
            'result': result
        }
        self.queries.append(query_info)
        self._log(f"📊 Запрос #{self.query_count}: {query[:50]}...")
        if params:
            self._log(f"   Параметры: {params}")
    
    def stop(self):
        """Остановка монитора"""
        self.running = False
        self._log("🛑 Мониторинг базы данных остановлен")
    
    def get_stats(self):
        """Получить статистику"""
        return {
            'total_queries': self.query_count,
            'recent_queries': self.queries[-5:] if self.queries else []
        }