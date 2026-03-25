# -*- coding: utf-8 -*-

"""Тесты моделей данных (Client, Matrix)"""
import pytest
from database.models import Client, Matrix


class TestMatrix:
    """Тесты модели Matrix."""

    def test_from_db_row_sqlite(self, sample_matrix_row):
        """from_db_row корректно десериализует sqlite3.Row."""
        m = Matrix.from_db_row(sample_matrix_row)
        assert m.id == 1
        assert m.name == "Матрица Х"
        assert m.price == 5000.0
        assert m.created_date == "2025-01-01 00:00:00"

    def test_from_db_row_tuple(self):
        """from_db_row корректно десериализует tuple."""
        m = Matrix.from_db_row((42, "Tuple", 999.0, "2025-06-01"))
        assert m.id == 42
        assert m.name == "Tuple"
        assert m.price == 999.0

    def test_to_dict(self):
        """to_dict возвращает полный словарь."""
        m = Matrix(id=1, name="X", price=100.0, created_date="2025-01-01")
        d = m.to_dict()
        assert isinstance(d, dict)
        assert d["id"] == 1
        assert d["name"] == "X"
        assert d["price"] == 100.0
        assert d["created_date"] == "2025-01-01"

    def test_to_dict_roundtrip(self):
        """to_dict → Matrix(**dict) — данные не теряются."""
        original = Matrix(id=5, name="Рунд", price=7777.0, created_date="2025-06-15")
        d = original.to_dict()
        restored = Matrix(**d)
        assert restored == original


class TestClient:
    """Тесты модели Client."""

    def test_from_db_row_sqlite(self, sample_sqlite_row):
        """from_db_row корректно десериализует sqlite3.Row."""
        c = Client.from_db_row(sample_sqlite_row)
        assert c.id == 1
        assert c.name == "Тест Тестов"
        assert c.telegram == "@test"
        assert c.birth_date == "01.01.2000"
        assert c.destiny_number == 4
        assert c.matrix_id is None
        assert c.service_price == 1000.0
        assert c.is_completed is False
        assert c.matrix_name is None

    def test_from_db_row_tuple_minimal(self):
        """from_db_row обрабатывает короткий tuple с дефолтами."""
        row = (10, "Имя", "@tg", "01.01.1990", 5, None, "Сервис", 2000.0)
        c = Client.from_db_row(row)
        assert c.id == 10
        assert c.name == "Имя"
        assert c.comment is None
        assert c.phone is None
        assert c.is_completed is False

    def test_from_db_row_tuple_full(self):
        """from_db_row обрабатывает полный tuple."""
        row = (
            1, "Full", "@full", "15.03.1985", 8, 2,
            "Service", 5000.0, "Comment", "+70001112233",
            "01.06.2025", "2025-06-01 10:00:00", 1, "01.06.2025", "Matrix A"
        )
        c = Client.from_db_row(row)
        assert c.is_completed is True
        assert c.completed_date == "01.06.2025"
        assert c.matrix_name == "Matrix A"

    def test_formatted_price(self):
        """formatted_price форматирует число с пробелами."""
        c = Client(
            id=1, name="X", telegram=None, birth_date="01.01.2000",
            destiny_number=4, matrix_id=None, service_name="S",
            service_price=15000.0, comment=None, phone=None,
            order_date="01.01.2025", created_date="2025-01-01",
            is_completed=False, completed_date=None,
        )
        assert c.formatted_price == "15 000 руб."

    def test_formatted_price_zero(self):
        """formatted_price для нулевой цены."""
        c = Client(
            id=1, name="X", telegram=None, birth_date="01.01.2000",
            destiny_number=0, matrix_id=None, service_name="S",
            service_price=0, comment=None, phone=None,
            order_date="01.01.2025", created_date="2025-01-01",
            is_completed=False, completed_date=None,
        )
        assert c.formatted_price == "0 руб."

    def test_status_emoji_pending(self):
        """status_emoji для невыполненного заказа."""
        c = Client(
            id=1, name="X", telegram=None, birth_date="01.01.2000",
            destiny_number=0, matrix_id=None, service_name="S",
            service_price=0, comment=None, phone=None,
            order_date="01.01.2025", created_date="2025-01-01",
            is_completed=False, completed_date=None,
        )
        assert c.status_emoji == "⏳"
        assert c.status_text == "В ожидании"

    def test_status_emoji_completed(self):
        """status_emoji для выполненного заказа."""
        c = Client(
            id=1, name="X", telegram=None, birth_date="01.01.2000",
            destiny_number=0, matrix_id=None, service_name="S",
            service_price=0, comment=None, phone=None,
            order_date="01.01.2025", created_date="2025-01-01",
            is_completed=True, completed_date="01.01.2025",
        )
        assert c.status_emoji == "✅"
        assert c.status_text == "Выполнен"

    def test_to_dict_contains_all_keys(self):
        """to_dict содержит все ключи."""
        c = Client(
            id=1, name="Dict", telegram="@d", birth_date="01.01.2000",
            destiny_number=4, matrix_id=2, service_name="S",
            service_price=100.0, comment="C", phone="+7",
            order_date="01.01.2025", created_date="2025-01-01",
            is_completed=False, completed_date=None, matrix_name="M",
        )
        d = c.to_dict()
        expected_keys = {
            "id", "name", "telegram", "birth_date", "destiny_number",
            "matrix_id", "matrix_name", "service_name", "service_price",
            "comment", "phone", "order_date", "created_date",
            "is_completed", "completed_date", "status",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_status_field(self):
        """to_dict включает computed-поле status."""
        c = Client(
            id=1, name="X", telegram=None, birth_date="01.01.2000",
            destiny_number=0, matrix_id=None, service_name="S",
            service_price=0, comment=None, phone=None,
            order_date="01.01.2025", created_date="2025-01-01",
            is_completed=True, completed_date=None,
        )
        assert c.to_dict()["status"] == "Выполнен"
