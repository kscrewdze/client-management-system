# -*- coding: utf-8 -*-

"""Фрейм просмотра базы данных — SQL-браузер в стиле профессиональных IDE."""
import logging
import sqlite3
from typing import Any, List, Optional

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QComboBox, QTableView, QHeaderView,
    QAbstractItemView, QLineEdit, QSplitter,
)

logger = logging.getLogger(__name__)


class RawTableModel(QAbstractTableModel):
    """Универсальная модель для произвольных SQL-данных."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._headers: List[str] = []
        self._rows: List[list] = []

    def load(self, headers: List[str], rows: List[list]) -> None:
        self.beginResetModel()
        self._headers = headers
        self._rows = rows
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            val = self._rows[index.row()][index.column()]
            return "" if val is None else str(val)
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignLeft | Qt.AlignVCenter)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section] if section < len(self._headers) else ""
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)
        return None


class DatabaseFrame(QWidget):
    """Фрейм-браузер базы данных."""

    def __init__(self, db: Any, notifier: Any) -> None:
        super().__init__()
        self.db = db
        self.notifier = notifier
        self._create_widgets()
        self._load_tables()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Заголовок
        top = QHBoxLayout()
        top.setSpacing(8)
        title = QLabel("БАЗА ДАННЫХ")
        title.setProperty("cssClass", "title")
        top.addWidget(title)
        top.addStretch()

        # Выбор таблицы
        tbl_label = QLabel("Таблица:")
        tbl_label.setProperty("cssClass", "hint")
        top.addWidget(tbl_label)
        self._table_combo = QComboBox()
        self._table_combo.setFixedWidth(180)
        self._table_combo.setFixedHeight(28)
        self._table_combo.currentTextChanged.connect(self._on_table_selected)
        top.addWidget(self._table_combo)

        # Фильтр
        self._filter = QLineEdit()
        self._filter.setPlaceholderText("🔍 Фильтр по значению...")
        self._filter.setFixedWidth(220)
        self._filter.setFixedHeight(28)
        self._filter.textChanged.connect(self._apply_filter)
        top.addWidget(self._filter)

        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setProperty("cssClass", "info")
        refresh_btn.setFixedHeight(28)
        refresh_btn.setToolTip("Перезагрузить данные таблицы")
        refresh_btn.clicked.connect(self._reload_data)
        top.addWidget(refresh_btn)
        layout.addLayout(top)

        # Разделитель: информация + таблица
        splitter = QSplitter(Qt.Vertical)

        # Инфо-панель
        info_frame = QFrame()
        info_frame.setProperty("cssClass", "card")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(10, 4, 10, 4)

        self._info_db = QLabel("—")
        self._info_db.setProperty("cssClass", "hint")
        info_layout.addWidget(self._info_db)
        info_layout.addStretch()

        self._info_rows = QLabel("—")
        self._info_rows.setProperty("cssClass", "hint")
        info_layout.addWidget(self._info_rows)
        info_layout.addStretch()

        self._info_cols = QLabel("—")
        self._info_cols.setProperty("cssClass", "hint")
        info_layout.addWidget(self._info_cols)

        splitter.addWidget(info_frame)

        # Таблица данных
        self._model = RawTableModel(self)
        self._all_rows: List[list] = []
        self._all_headers: List[str] = []

        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSortingEnabled(True)
        self._table.setShowGrid(True)
        self._table.verticalHeader().setVisible(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.horizontalHeader().setStretchLastSection(True)

        splitter.addWidget(self._table)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, stretch=1)

        # Статус
        self._status = QLabel("")
        self._status.setProperty("cssClass", "hint")
        layout.addWidget(self._status)

    def _load_tables(self) -> None:
        """Загрузить список таблиц из SQLite."""
        try:
            with self.db._lock:
                cursor = self.db.conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                tables = [row[0] for row in cursor.fetchall()]
            self._table_combo.blockSignals(True)
            self._table_combo.clear()
            for t in tables:
                self._table_combo.addItem(t)
            self._table_combo.blockSignals(False)

            self._info_db.setText(f"📁 {self.db.db_path.name}")

            if tables:
                self._table_combo.setCurrentIndex(0)
                self._on_table_selected(tables[0])
        except Exception as e:
            logger.error("Ошибка загрузки таблиц: %s", e)

    def _on_table_selected(self, table_name: str) -> None:
        """Загрузить данные выбранной таблицы."""
        if not table_name:
            return
        try:
            # Безопасная проверка имени таблицы (только буквы, цифры, _)
            if not all(c.isalnum() or c == '_' for c in table_name):
                self.notifier.show_error("Недопустимое имя таблицы")
                return

            with self.db._lock:
                cursor = self.db.conn.execute(f'SELECT * FROM "{table_name}"')
                self._all_headers = [desc[0] for desc in cursor.description]
                self._all_rows = [list(row) for row in cursor.fetchall()]

            self._model.load(self._all_headers, self._all_rows)
            self._info_rows.setText(f"Строк: {len(self._all_rows)}")
            self._info_cols.setText(f"Колонок: {len(self._all_headers)}")
            self._status.setText(f"Таблица: {table_name}")
            self._filter.clear()

            # Автоширина колонок
            header = self._table.horizontalHeader()
            for i in range(len(self._all_headers)):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            if self._all_headers:
                header.setSectionResizeMode(
                    len(self._all_headers) - 1, QHeaderView.Stretch,
                )
        except Exception as e:
            logger.error("Ошибка загрузки таблицы %s: %s", table_name, e)
            self.notifier.show_error(f"Ошибка: {e}")

    def _apply_filter(self, text: str) -> None:
        """Фильтровать строки по вхождению текста."""
        text = text.strip().lower()
        if not text:
            self._model.load(self._all_headers, self._all_rows)
            self._info_rows.setText(f"Строк: {len(self._all_rows)}")
            return

        filtered = [
            row for row in self._all_rows
            if any(text in str(cell).lower() for cell in row)
        ]
        self._model.load(self._all_headers, filtered)
        self._info_rows.setText(f"Строк: {len(filtered)} / {len(self._all_rows)}")

    def _reload_data(self) -> None:
        table = self._table_combo.currentText()
        if table:
            self._on_table_selected(table)

    def refresh(self) -> None:
        self._load_tables()
