# -*- coding: utf-8 -*-

"""Тесты статистики"""
import pytest


class TestStatistics:
    """Тесты модуля статистики."""

    def test_empty_db(self, db):
        """Статистика пустой БД — все нули."""
        stats = db.get_statistics()
        assert stats["total_clients"] == 0
        assert stats["total_earnings"] == 0
        assert stats["completed_count"] == 0
        assert stats["completed_earnings"] == 0
        assert stats["average_price"] == 0
        assert stats["matrices_count"] == 0

    def test_with_data(self, db_with_client, sample_client_data):
        """Статистика после добавления данных."""
        database, cid, mid = db_with_client
        stats = database.get_statistics()
        assert stats["total_clients"] == 1
        assert stats["total_earnings"] == sample_client_data["service_price"]
        assert stats["completed_count"] == 0
        assert stats["matrices_count"] == 1

    def test_after_toggle(self, db_with_client, sample_client_data):
        """Статистика учитывает выполненных клиентов."""
        database, cid, _ = db_with_client
        database.toggle_completed(cid)
        stats = database.get_statistics()
        assert stats["completed_count"] == 1
        assert stats["completed_earnings"] == sample_client_data["service_price"]

    def test_average_price(self, db, sample_client_data):
        """Средняя цена корректно рассчитывается."""
        data1 = sample_client_data.copy()
        data1["service_price"] = 1000.0
        data2 = sample_client_data.copy()
        data2["service_price"] = 3000.0
        db.add_client(data1)
        db.add_client(data2)
        stats = db.get_statistics()
        assert stats["average_price"] == 2000.0
