# -*- coding: utf-8 -*-

"""Работа с матрицами в БД"""
from datetime import datetime
import sqlite3
from typing import List, Optional

from database.models import Matrix


class MatricesDB:
    """Класс для работы с матрицами"""
    
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor
        self.conn = db.conn
    
    def add_matrix(self, name: str, price: float) -> Optional[int]:
        """Добавление новой матрицы"""
        try:
            self.cursor.execute('''
                INSERT INTO matrices (name, price, created_date)
                VALUES (?, ?, ?)
            ''', (name, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()
            matrix_id = self.cursor.lastrowid
            print(f"✅ Добавлена матрица: {name} (ID: {matrix_id})")
            return matrix_id
        except sqlite3.IntegrityError:
            print(f"⚠️ Матрица уже существует: {name}")
            return None
    
    def get_all_matrices(self) -> List[Matrix]:
        """Получение всех матриц"""
        self.cursor.execute('SELECT * FROM matrices ORDER BY name')
        matrices = [Matrix.from_db_row(row) for row in self.cursor.fetchall()]
        print(f"📊 Загружено матриц: {len(matrices)}")
        return matrices
    
    def get_matrix_by_id(self, matrix_id: int) -> Optional[Matrix]:
        """Получение матрицы по ID"""
        self.cursor.execute('SELECT * FROM matrices WHERE id = ?', (matrix_id,))
        row = self.cursor.fetchone()
        return Matrix.from_db_row(row) if row else None
    
    def update_matrix(self, matrix_id: int, name: str, price: float):
        """Обновление матрицы"""
        self.cursor.execute('''
            UPDATE matrices 
            SET name=?, price=?
            WHERE id=?
        ''', (name, price, matrix_id))
        self.conn.commit()
        print(f"✅ Обновлена матрица ID {matrix_id}: {name}")
    
    def delete_matrix(self, matrix_id: int):
        """Удаление матрицы"""
        self.cursor.execute('UPDATE clients SET matrix_id = NULL WHERE matrix_id = ?', (matrix_id,))
        self.cursor.execute('DELETE FROM matrices WHERE id = ?', (matrix_id,))
        self.conn.commit()
        print(f"✅ Удалена матрица ID {matrix_id}")