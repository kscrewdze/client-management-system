# -*- coding: utf-8 -*-

"""Работа с матрицами в БД"""
import logging
from datetime import datetime
import sqlite3
from typing import List, Optional

from database.models import Matrix

logger = logging.getLogger(__name__)


class MatricesDB:
    """Класс для работы с матрицами"""
    
    def __init__(self, db):
        self.db = db
    
    def add_matrix(self, name: str, price: float) -> Optional[int]:
        """Добавление новой матрицы"""
        try:
            with self.db._lock:
                self.db.cursor.execute('''
                    INSERT INTO matrices (name, price, created_date)
                    VALUES (?, ?, ?)
                ''', (name, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.db.conn.commit()
                matrix_id = self.db.cursor.lastrowid
            logger.debug("Добавлена матрица: %s (ID: %d)", name, matrix_id)
            return matrix_id
        except sqlite3.IntegrityError:
            logger.warning("Матрица уже существует: %s", name)
            return None
    
    def get_all_matrices(self) -> List[Matrix]:
        """Получение всех матриц"""
        with self.db._lock:
            self.db.cursor.execute('SELECT * FROM matrices ORDER BY name')
            matrices = [Matrix.from_db_row(row) for row in self.db.cursor.fetchall()]
        logger.debug("Загружено матриц: %d", len(matrices))
        return matrices
    
    def get_matrix_by_id(self, matrix_id: int) -> Optional[Matrix]:
        """Получение матрицы по ID"""
        with self.db._lock:
            self.db.cursor.execute('SELECT * FROM matrices WHERE id = ?', (matrix_id,))
            row = self.db.cursor.fetchone()
        return Matrix.from_db_row(row) if row else None
    
    def update_matrix(self, matrix_id: int, name: str, price: float):
        """Обновление матрицы"""
        with self.db._lock:
            self.db.cursor.execute('''
                UPDATE matrices 
                SET name=?, price=?
                WHERE id=?
            ''', (name, price, matrix_id))
            self.db.conn.commit()
        logger.debug("Обновлена матрица ID %d: %s", matrix_id, name)
    
    def delete_matrix(self, matrix_id: int):
        """Удаление матрицы"""
        with self.db._lock:
            self.db.cursor.execute('UPDATE clients SET matrix_id = NULL WHERE matrix_id = ?', (matrix_id,))
            self.db.cursor.execute('DELETE FROM matrices WHERE id = ?', (matrix_id,))
            self.db.conn.commit()
        logger.debug("Удалена матрица ID %d", matrix_id)
