# -*- coding: utf-8 -*-

"""Базовый класс для работы с БД
Автор: kScrewdze
Версия: 9.0
"""

import sqlite3
import logging
import threading
from typing import Optional

from config.settings import Settings
from database.utils import calculate_destiny_number
from database.clients import ClientsDB
from database.matrices import MatricesDB
from database.search import SearchDB
from database.statistics import StatisticsDB

logger = logging.getLogger(__name__)


class Database:
    """Основной класс для работы с базой данных"""
    
    def __init__(self):
        self.db_path = Settings.DB_PATH
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self._lock = threading.Lock()

        # Инициализация
        self.connect()
        self.create_tables()
        self.update_table_structure()

        # Инициализация подмодулей
        self.clients = ClientsDB(self)
        self.matrices = MatricesDB(self)
        self.search = SearchDB(self)
        self.statistics = StatisticsDB(self)

        logger.info("База данных инициализирована: %s", self.db_path)
    
    @staticmethod
    def _unicode_lower(value: str | None) -> str | None:
        """Unicode-совместимый LOWER для SQLite (кириллица и др.)."""
        return value.lower() if value else value

    def connect(self) -> None:
        """Установка соединения с базой данных."""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        # Регистрируем Unicode-совместимый LOWER для кириллицы
        self.conn.create_function("UNICODE_LOWER", 1, self._unicode_lower, deterministic=True)
        self.cursor = self.conn.cursor()
        logger.debug("Соединение с БД установлено: %s", self.db_path)
    
    def reconnect(self) -> None:
        """Переподключение к базе данных (для работы с потоками)."""
        with self._lock:
            try:
                if self.conn:
                    self.conn.close()
            except sqlite3.Error as e:
                logger.warning("Ошибка закрытия соединения при переподключении: %s", e)
            self.connect()
        logger.info("Переподключение к БД выполнено")
    
    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        if self.conn:
            try:
                self.conn.close()
                logger.info("Соединение с БД закрыто")
            except sqlite3.Error as e:
                logger.error("Ошибка при закрытии соединения с БД: %s", e)
    
    def create_tables(self):
        """Создание таблиц клиентов и матриц"""
        # Таблица матриц
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matrices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                created_date TEXT NOT NULL
            )
        ''')
        
        # Таблица клиентов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                telegram TEXT,
                birth_date TEXT NOT NULL,
                destiny_number INTEGER NOT NULL DEFAULT 0,
                matrix_id INTEGER,
                service_name TEXT,
                service_price REAL NOT NULL,
                comment TEXT,
                phone TEXT,
                order_date TEXT NOT NULL,
                created_date TEXT NOT NULL,
                is_completed INTEGER DEFAULT 0,
                completed_date TEXT,
                FOREIGN KEY (matrix_id) REFERENCES matrices(id)
            )
        ''')
        
        self.conn.commit()
        logger.debug("Таблицы созданы или уже существуют")

    
    def update_table_structure(self):
        """Обновление структуры таблицы"""
        self.cursor.execute("PRAGMA table_info(clients)")
        existing_columns = [column[1] for column in self.cursor.fetchall()]
        
        new_columns = [
            ('phone', 'TEXT'),
            ('comment', 'TEXT'),
            ('order_date', 'TEXT'),
            ('destiny_number', 'INTEGER DEFAULT 0'),
            ('is_completed', 'INTEGER DEFAULT 0'),
            ('completed_date', 'TEXT'),
            ('matrix_id', 'INTEGER'),
            ('service_name', 'TEXT')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    # column_name и column_type — внутренние константы, не пользовательский ввод
                    self.cursor.execute(
                        f'ALTER TABLE clients ADD COLUMN {column_name} {column_type}'
                    )
                    self.conn.commit()
                    logger.info("Добавлена колонка: %s", column_name)
                except sqlite3.Error as e:
                    logger.error("Ошибка добавления колонки %s: %s", column_name, e)
    
    # Делегирование методов для обратной совместимости
    def calculate_destiny_number(self, birth_date: str) -> int:
        """Расчет числа судьбы"""
        return calculate_destiny_number(birth_date)
    
    # Методы для работы с матрицами
    def add_matrix(self, name: str, price: float) -> Optional[int]:
        return self.matrices.add_matrix(name, price)
    
    def get_all_matrices(self):
        return self.matrices.get_all_matrices()
    
    def get_matrix_by_id(self, matrix_id: int):
        return self.matrices.get_matrix_by_id(matrix_id)
    
    def update_matrix(self, matrix_id: int, name: str, price: float):
        return self.matrices.update_matrix(matrix_id, name, price)
    
    def delete_matrix(self, matrix_id: int):
        return self.matrices.delete_matrix(matrix_id)
    
    # Методы для работы с клиентами
    def add_client(self, client_data):
        return self.clients.add_client(client_data)
    
    def update_client(self, client_id, client_data):
        return self.clients.update_client(client_id, client_data)
    
    def delete_client(self, client_id):
        return self.clients.delete_client(client_id)
    
    def get_all_clients(self):
        return self.clients.get_all_clients()
    
    def get_client_by_id(self, client_id):
        return self.clients.get_client_by_id(client_id)
    
    def toggle_completed(self, client_id):
        return self.clients.toggle_completed(client_id)
    
    # Методы для поиска
    def search_clients(self, query: str):
        return self.search.search_clients(query)
    
    # Методы для статистики
    def get_statistics(self):
        return self.statistics.get_statistics()