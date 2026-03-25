# -*- coding: utf-8 -*-

"""Фрейм управления матрицами — компактный."""
import logging
from typing import Any, Callable, List, Optional

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableView, QHeaderView, QAbstractItemView,
)

from database.models import Matrix
from gui_qt.helpers import fmt_price
from gui_qt.widgets import ConfirmDialog

logger = logging.getLogger(__name__)

_M_COLS = [("Название матрицы", 0), ("Цена", 140), ("Дата создания", 140)]


class MatrixTableModel(QAbstractTableModel):
    """Модель таблицы матриц."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._data: List[Matrix] = []

    def set_data(self, rows: List[Matrix]) -> None:
        self.beginResetModel()
        self._data = rows
        self.endResetModel()

    def matrix_at(self, row: int) -> Optional[Matrix]:
        return self._data[row] if 0 <= row < len(self._data) else None

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(_M_COLS)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        m = self._data[index.row()]
        col = index.column()
        if role == Qt.DisplayRole:
            return [m.name, fmt_price(m.price), (m.created_date or "—")[:10]][col]
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignCenter) if col else int(Qt.AlignLeft | Qt.AlignVCenter)
        if role == Qt.UserRole:
            return m.id
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return _M_COLS[section][0]
        return None


class MatricesFrame(QWidget):
    """Фрейм управления матрицами."""

    def __init__(self, db: Any, notifier: Any, refresh_callback: Callable) -> None:
        super().__init__()
        self.db = db
        self.notifier = notifier
        self.refresh_callback = refresh_callback
        self._create_widgets()
        self.refresh()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        top = QHBoxLayout()
        top.setSpacing(8)
        title = QLabel("УПРАВЛЕНИЕ МАТРИЦАМИ")
        title.setProperty("cssClass", "title")
        top.addWidget(title)
        top.addStretch()

        for text, cls, handler, tooltip in [
            ("➕ Добавить", "success", self._add_matrix, "Добавить матрицу"),
            ("✏️ Редактировать", "warning", self._edit_selected, "Редактировать выбранную"),
            ("🗑 Удалить", "danger", self._delete_selected, "Удалить выбранную"),
        ]:
            b = QPushButton(text)
            b.setProperty("cssClass", cls)
            b.setFixedHeight(28)
            b.setToolTip(tooltip)
            b.clicked.connect(handler)
            top.addWidget(b)
        layout.addLayout(top)

        self._model = MatrixTableModel(self)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setSortingEnabled(True)
        self._table.setShowGrid(False)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self._table.horizontalHeader()
        for i, (_, w) in enumerate(_M_COLS):
            if w == 0:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                self._table.setColumnWidth(i, w)

        self._table.doubleClicked.connect(lambda _: self._edit_selected())
        layout.addWidget(self._table, stretch=1)

    def refresh(self) -> None:
        try:
            self._model.set_data(self.db.get_all_matrices() or [])
        except Exception as e:
            logger.error("Ошибка загрузки матриц: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")

    def _selected_matrix(self) -> Optional[Matrix]:
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            self.notifier.show_warning("Выберите матрицу")
            return None
        return self._model.matrix_at(rows[0].row())

    def _add_matrix(self) -> None:
        from gui_qt.dialogs.matrix_dialog import MatrixDialog
        dlg = MatrixDialog(self.window(), self.notifier)
        if dlg.exec():
            name, price = dlg.result
            if self.db.add_matrix(name, price):
                self.notifier.show_success(f"Матрица '{name}' добавлена")
                self.refresh()
                self.refresh_callback()
            else:
                self.notifier.show_error("Матрица уже существует")

    def _edit_selected(self) -> None:
        m = self._selected_matrix()
        if not m:
            return
        from gui_qt.dialogs.matrix_dialog import MatrixDialog
        dlg = MatrixDialog(
            self.window(), self.notifier,
            matrix_id=m.id, matrix_data=(m.id, m.name, m.price),
        )
        if dlg.exec():
            name, price = dlg.result
            self.db.update_matrix(m.id, name, price)
            self.notifier.show_success(f"Матрица '{name}' обновлена")
            self.refresh()
            self.refresh_callback()

    def _delete_selected(self) -> None:
        m = self._selected_matrix()
        if not m:
            return
        if ConfirmDialog.confirm(self, "Подтверждение", f"Удалить '{m.name}'?"):
            self.db.delete_matrix(m.id)
            self.notifier.show_success("Матрица удалена")
            self.refresh()
            self.refresh_callback()
