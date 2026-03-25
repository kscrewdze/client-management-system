# -*- coding: utf-8 -*-

"""Общие фикстуры для тестов"""
import sys
import sqlite3
from pathlib import Path
from unittest.mock import patch
from datetime import datetime

import pytest

# Добавляем корень проекта в sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def db():
    """In-memory БД с инициализированными таблицами."""
    with patch("config.settings.Settings.DB_PATH", ":memory:"):
        from database.core import Database
        database = Database()
        yield database
        database.close()


@pytest.fixture()
def db_with_matrix(db):
    """БД с одной предустановленной матрицей."""
    matrix_id = db.add_matrix("Тестовая матрица", 5000.0)
    return db, matrix_id


@pytest.fixture()
def sample_client_data():
    """Минимальный набор данных для добавления клиента."""
    return {
        "name": "Иван Петров",
        "telegram": "@ivan_test",
        "birth_date": "26.01.1982",
        "destiny_number": 11,
        "matrix_id": None,
        "service_name": "Тестовая услуга",
        "service_price": 3000.0,
        "comment": "Тестовый комментарий",
        "phone": "+79001234567",
        "order_date": "15.06.2025",
    }


@pytest.fixture()
def db_with_client(db_with_matrix, sample_client_data):
    """БД с одной матрицей и одним клиентом."""
    database, matrix_id = db_with_matrix
    sample_client_data["matrix_id"] = matrix_id
    client_id = database.add_client(sample_client_data)
    return database, client_id, matrix_id


@pytest.fixture()
def sample_sqlite_row():
    """sqlite3.Row для тестов модели Client."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE t (
            id INTEGER, name TEXT, telegram TEXT, birth_date TEXT,
            destiny_number INTEGER, matrix_id INTEGER,
            service_name TEXT, service_price REAL,
            comment TEXT, phone TEXT, order_date TEXT,
            created_date TEXT, is_completed INTEGER,
            completed_date TEXT, matrix_name TEXT
        )
    """)
    cur.execute("""
        INSERT INTO t VALUES (
            1, 'Тест Тестов', '@test', '01.01.2000', 4, NULL,
            'Услуга', 1000.0, 'Комм', '+70001112233', '10.01.2025',
            '2025-01-10 12:00:00', 0, NULL, NULL
        )
    """)
    cur.execute("SELECT * FROM t")
    row = cur.fetchone()
    yield row
    conn.close()


@pytest.fixture()
def sample_matrix_row():
    """sqlite3.Row для тестов модели Matrix."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("CREATE TABLE t (id INTEGER, name TEXT, price REAL, created_date TEXT)")
    cur.execute("INSERT INTO t VALUES (1, 'Матрица Х', 5000.0, '2025-01-01 00:00:00')")
    cur.execute("SELECT * FROM t")
    row = cur.fetchone()
    yield row
    conn.close()
