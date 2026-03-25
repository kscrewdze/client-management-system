# -*- coding: utf-8 -*-

"""Тесты поиска и фильтров"""
import pytest
from database.models import Client
from utils.search.filters import SearchFilters


def _make_client(**overrides) -> Client:
    """Хелпер для создания клиента с дефолтами."""
    defaults = dict(
        id=1, name="Тест", telegram=None, birth_date="01.01.2000",
        destiny_number=4, matrix_id=None, service_name="S",
        service_price=1000.0, comment=None, phone=None,
        order_date="01.01.2025", created_date="2025-01-01",
        is_completed=False, completed_date=None, matrix_name=None,
    )
    defaults.update(overrides)
    return Client(**defaults)


class TestSearchDB:
    """Тесты поиска по БД."""

    def test_search_by_name(self, db_with_client):
        """Поиск по имени."""
        database, _, _ = db_with_client
        results = database.search_clients("Иван")
        assert len(results) == 1
        assert results[0].name == "Иван Петров"

    def test_search_by_telegram(self, db_with_client):
        """Поиск по telegram."""
        database, _, _ = db_with_client
        results = database.search_clients("ivan_test")
        assert len(results) == 1

    def test_search_by_phone(self, db_with_client):
        """Поиск по телефону."""
        database, _, _ = db_with_client
        results = database.search_clients("9001234567")
        assert len(results) == 1

    def test_search_by_comment(self, db_with_client):
        """Поиск по комментарию."""
        database, _, _ = db_with_client
        results = database.search_clients("Тестовый комментарий")
        assert len(results) == 1

    def test_search_no_results(self, db_with_client):
        """Несуществующий запрос — пустой список."""
        database, _, _ = db_with_client
        results = database.search_clients("несуществующий_запрос_xyz")
        assert results == []

    def test_search_case_insensitive_ascii(self, db_with_client, sample_client_data):
        """LIKE нечувствителен к регистру для ASCII."""
        database, _, _ = db_with_client
        # Добавляем клиента с ASCII-именем
        data = sample_client_data.copy()
        data["name"] = "John Doe"
        database.add_client(data)
        results = database.search_clients("john")
        assert len(results) == 1

    def test_search_cyrillic_case_insensitive(self, db_with_client):
        """UNICODE_LOWER обеспечивает case-insensitive поиск для кириллицы."""
        database, _, _ = db_with_client
        # "Иван Петров" в БД, ищем "иван" в нижнем регистре
        results = database.search_clients("иван")
        assert len(results) == 1
        assert results[0].name == "Иван Петров"

    def test_search_empty_db(self, db):
        """Поиск в пустой БД — пустой список."""
        assert db.search_clients("test") == []


class TestSearchFiltersByStatus:
    """Фильтрация по статусу."""

    def test_show_all(self):
        clients = [
            _make_client(id=1, is_completed=True),
            _make_client(id=2, is_completed=False),
        ]
        result = SearchFilters.by_status(clients, show_completed=True, show_pending=True)
        assert len(result) == 2

    def test_show_only_completed(self):
        clients = [
            _make_client(id=1, is_completed=True),
            _make_client(id=2, is_completed=False),
        ]
        result = SearchFilters.by_status(clients, show_completed=True, show_pending=False)
        assert len(result) == 1
        assert result[0].id == 1

    def test_show_only_pending(self):
        clients = [
            _make_client(id=1, is_completed=True),
            _make_client(id=2, is_completed=False),
        ]
        result = SearchFilters.by_status(clients, show_completed=False, show_pending=True)
        assert len(result) == 1
        assert result[0].id == 2


class TestSearchFiltersByPrice:
    """Фильтрация по диапазону цен."""

    def test_no_filter(self):
        clients = [_make_client(service_price=100)]
        assert SearchFilters.by_price_range(clients) == clients

    def test_min_price(self):
        clients = [
            _make_client(id=1, service_price=500),
            _make_client(id=2, service_price=2000),
        ]
        result = SearchFilters.by_price_range(clients, min_price=1000)
        assert len(result) == 1
        assert result[0].id == 2

    def test_max_price(self):
        clients = [
            _make_client(id=1, service_price=500),
            _make_client(id=2, service_price=2000),
        ]
        result = SearchFilters.by_price_range(clients, max_price=1000)
        assert len(result) == 1
        assert result[0].id == 1

    def test_range(self):
        clients = [
            _make_client(id=1, service_price=500),
            _make_client(id=2, service_price=1500),
            _make_client(id=3, service_price=3000),
        ]
        result = SearchFilters.by_price_range(clients, min_price=1000, max_price=2000)
        assert len(result) == 1
        assert result[0].id == 2


class TestSearchFiltersByDate:
    """Фильтрация по диапазону дат."""

    def test_no_filter(self):
        clients = [_make_client(order_date="01.01.2025")]
        assert SearchFilters.by_date_range(clients) == clients

    def test_start_date(self):
        clients = [
            _make_client(id=1, order_date="01.01.2025"),
            _make_client(id=2, order_date="15.06.2025"),
        ]
        result = SearchFilters.by_date_range(clients, start_date="01.06.2025")
        assert len(result) == 1
        assert result[0].id == 2
