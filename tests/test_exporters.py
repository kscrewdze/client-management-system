# -*- coding: utf-8 -*-

"""Тесты авто-экспорта в Excel"""
import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch


class TestExportClients:
    """Экспорт клиентов в xlsx."""

    def test_export_creates_file(self, db_with_client):
        """export_clients создаёт файл xlsx."""
        database, _, _ = db_with_client
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("gui_qt.exporters._DIR", Path(tmpdir)):
                from gui_qt.exporters import export_clients
                path = export_clients(database)
                assert path.exists()
                assert path.suffix == ".xlsx"
                assert path.stat().st_size > 0

    def test_export_empty_db(self, db):
        """Экспорт пустой БД тоже создаёт файл (только заголовки)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("gui_qt.exporters._DIR", Path(tmpdir)):
                from gui_qt.exporters import export_clients
                path = export_clients(db)
                assert path.exists()


class TestExportMatrices:
    """Экспорт матриц в xlsx."""

    def test_export_creates_file(self, db_with_matrix):
        """export_matrices создаёт файл xlsx."""
        database, _ = db_with_matrix
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("gui_qt.exporters._DIR", Path(tmpdir)):
                from gui_qt.exporters import export_matrices
                path = export_matrices(database)
                assert path.exists()
                assert path.suffix == ".xlsx"

    def test_export_empty_db(self, db):
        """Экспорт пустой БД — файл с одними заголовками."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("gui_qt.exporters._DIR", Path(tmpdir)):
                from gui_qt.exporters import export_matrices
                path = export_matrices(db)
                assert path.exists()


class TestAutoExportAll:
    """auto_export_all не падает."""

    def test_auto_export(self, db_with_client):
        """auto_export_all создаёт оба файла."""
        database, _, _ = db_with_client
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            with patch("gui_qt.exporters._DIR", tmp):
                from gui_qt.exporters import auto_export_all
                auto_export_all(database)
                assert (tmp / "clients.xlsx").exists()
                assert (tmp / "matrices.xlsx").exists()
