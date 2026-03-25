# -*- coding: utf-8 -*-

"""Тесты CRUD-операций БД: клиенты и матрицы"""
import pytest
from database.models import Client, Matrix


class TestMatricesCRUD:
    """CRUD-операции с матрицами."""

    def test_add_matrix(self, db):
        """Добавление матрицы возвращает ID."""
        mid = db.add_matrix("Новая", 1000.0)
        assert mid is not None
        assert isinstance(mid, int)

    def test_get_all_matrices_empty(self, db):
        """Пустая БД — пустой список."""
        assert db.get_all_matrices() == []

    def test_get_all_matrices(self, db_with_matrix):
        """После добавления матрица появляется в списке."""
        database, _ = db_with_matrix
        matrices = database.get_all_matrices()
        assert len(matrices) == 1
        assert isinstance(matrices[0], Matrix)
        assert matrices[0].name == "Тестовая матрица"

    def test_get_matrix_by_id(self, db_with_matrix):
        """Получение матрицы по ID."""
        database, mid = db_with_matrix
        m = database.get_matrix_by_id(mid)
        assert m is not None
        assert m.id == mid
        assert m.name == "Тестовая матрица"

    def test_get_matrix_by_id_not_found(self, db):
        """Несуществующий ID возвращает None."""
        assert db.get_matrix_by_id(999) is None

    def test_update_matrix(self, db_with_matrix):
        """Обновление имени и цены матрицы."""
        database, mid = db_with_matrix
        database.update_matrix(mid, "Обновлённая", 7777.0)
        m = database.get_matrix_by_id(mid)
        assert m.name == "Обновлённая"
        assert m.price == 7777.0

    def test_delete_matrix(self, db_with_matrix):
        """Удаление матрицы убирает её из списка."""
        database, mid = db_with_matrix
        database.delete_matrix(mid)
        assert database.get_matrix_by_id(mid) is None
        assert database.get_all_matrices() == []

    def test_add_duplicate_matrix(self, db_with_matrix):
        """Повторное добавление матрицы с тем же именем возвращает None."""
        database, _ = db_with_matrix
        result = database.add_matrix("Тестовая матрица", 9999.0)
        assert result is None

    def test_delete_matrix_nullifies_client_fk(self, db_with_client):
        """Удаление матрицы обнуляет matrix_id у связанных клиентов."""
        database, cid, mid = db_with_client
        database.delete_matrix(mid)
        client = database.get_client_by_id(cid)
        assert client.matrix_id is None


class TestClientsCRUD:
    """CRUD-операции с клиентами."""

    def test_add_client(self, db, sample_client_data):
        """Добавление клиента возвращает ID."""
        cid = db.add_client(sample_client_data)
        assert isinstance(cid, int)
        assert cid > 0

    def test_get_all_clients_empty(self, db):
        """Пустая БД — пустой список клиентов."""
        assert db.get_all_clients() == []

    def test_get_all_clients(self, db_with_client):
        """После добавления клиент появляется в списке."""
        database, cid, _ = db_with_client
        clients = database.get_all_clients()
        assert len(clients) == 1
        assert isinstance(clients[0], Client)
        assert clients[0].id == cid

    def test_get_client_by_id(self, db_with_client):
        """Получение клиента по ID."""
        database, cid, _ = db_with_client
        c = database.get_client_by_id(cid)
        assert c is not None
        assert c.name == "Иван Петров"
        assert c.telegram == "@ivan_test"

    def test_get_client_by_id_not_found(self, db):
        """Несуществующий ID возвращает None."""
        assert db.get_client_by_id(999) is None

    def test_update_client(self, db_with_client, sample_client_data):
        """Обновление данных клиента."""
        database, cid, mid = db_with_client
        sample_client_data["name"] = "Обновлённый"
        sample_client_data["service_price"] = 9999.0
        database.update_client(cid, sample_client_data)
        c = database.get_client_by_id(cid)
        assert c.name == "Обновлённый"
        assert c.service_price == 9999.0

    def test_delete_client(self, db_with_client):
        """Удаление клиента."""
        database, cid, _ = db_with_client
        database.delete_client(cid)
        assert database.get_client_by_id(cid) is None
        assert database.get_all_clients() == []

    def test_toggle_completed(self, db_with_client):
        """toggle_completed переключает статус."""
        database, cid, _ = db_with_client
        # Изначально не выполнен
        c = database.get_client_by_id(cid)
        assert c.is_completed is False

        # Переключаем → выполнен
        result = database.toggle_completed(cid)
        assert result is True
        c = database.get_client_by_id(cid)
        assert c.is_completed is True
        assert c.completed_date is not None

        # Переключаем обратно → не выполнен
        result = database.toggle_completed(cid)
        assert result is False
        c = database.get_client_by_id(cid)
        assert c.is_completed is False
        assert c.completed_date is None

    def test_toggle_completed_nonexistent(self, db):
        """toggle_completed для несуществующего ID возвращает False."""
        assert db.toggle_completed(999) is False

    def test_client_has_matrix_name(self, db_with_client):
        """Клиент через JOIN получает matrix_name."""
        database, cid, _ = db_with_client
        c = database.get_client_by_id(cid)
        assert c.matrix_name == "Тестовая матрица"

    def test_add_multiple_clients(self, db, sample_client_data):
        """Добавление нескольких клиентов."""
        ids = []
        for i in range(5):
            data = sample_client_data.copy()
            data["name"] = f"Клиент {i}"
            ids.append(db.add_client(data))
        clients = db.get_all_clients()
        assert len(clients) == 5
        assert len(set(ids)) == 5  # все ID уникальны
