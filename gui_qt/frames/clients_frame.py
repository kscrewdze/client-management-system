# -*- coding: utf-8 -*-

"""Фрейм клиентов — QTableView + поиск + CRUD (компактный)."""
import logging
from typing import Any, Callable, List, Optional

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTableView, QHeaderView,
    QAbstractItemView, QApplication, QComboBox,
)

from database.models import Client
from gui_qt.helpers import fmt_price
from gui_qt.theme import theme_engine
from gui_qt.widgets import ConfirmDialog

logger = logging.getLogger(__name__)

_COLUMNS = [
    ("", 30), ("Имя", 0), ("Telegram", 110), ("Телефон", 110),
    ("Дата рожд.", 80), ("ЧС", 32), ("Матрица", 140),
    ("Цена", 75), ("Дата заказа", 80), ("Дата завершения", 95),
]


class ClientTableModel(QAbstractTableModel):
    """Табличная модель клиентов."""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._clients: List[Client] = []

    def set_clients(self, clients: List[Client]) -> None:
        self.beginResetModel()
        self._clients = clients
        self.endResetModel()

    def client_at(self, row: int) -> Optional[Client]:
        return self._clients[row] if 0 <= row < len(self._clients) else None

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._clients)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(_COLUMNS)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        c = self._clients[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            return [
                "✅" if c.is_completed else "",
                c.name,
                c.telegram or "—",
                c.phone or "—",
                c.birth_date,
                str(c.destiny_number),
                c.matrix_name or c.service_name or "—",
                fmt_price(c.service_price),
                c.order_date,
                c.completed_date or "—",
            ][col]

        if role == Qt.TextAlignmentRole:
            if col in (0, 4, 5, 8, 9):
                return int(Qt.AlignCenter)
            if col == 7:
                return int(Qt.AlignRight | Qt.AlignVCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)

        if role == Qt.BackgroundRole and c.is_completed:
            # Слегка зеленоватый фон для завершённых — через прозрачность от success
            tc = theme_engine.colors()
            base = QColor(tc.success)
            base.setAlpha(25)
            return base
        if role == Qt.ToolTipRole and c.comment:
            return f"💬 {c.comment}"
        if role == Qt.UserRole:
            return c.id
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return _COLUMNS[section][0]
        return None


class ClientsFrame(QWidget):
    """Фрейм со списком клиентов."""

    def __init__(self, db: Any, notifier: Any, refresh_callback: Callable) -> None:
        super().__init__()
        self.db = db
        self.notifier = notifier
        self.refresh_callback = refresh_callback

        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._do_search)

        self._create_widgets()
        self.refresh()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # Единая строка: кнопки + фильтр + поиск
        bar = QHBoxLayout()
        bar.setSpacing(4)

        for text, cls, handler, tooltip in [
            ("Обновить", "info", lambda: self.refresh(), "Обновить список (Ctrl+R)"),
            ("Редакт.", "warning", self.edit_selected, "Редактировать (Ctrl+E)"),
            ("Удалить", "danger", self.delete_selected, "Удалить (Ctrl+D)"),
            ("Отметить", "success", self.toggle_completed, "Отметить как выполнен"),
        ]:
            b = QPushButton(text)
            b.setProperty("cssClass", cls)
            b.setFixedHeight(26)
            b.setToolTip(tooltip)
            b.clicked.connect(handler)
            bar.addWidget(b)

        bar.addStretch()

        self._filter_combo = QComboBox()
        self._filter_combo.addItems(["Все", "Выполненные", "В ожидании"])
        self._filter_combo.setFixedWidth(120)
        self._filter_combo.setFixedHeight(26)
        self._filter_combo.currentIndexChanged.connect(lambda _: self.refresh())
        bar.addWidget(self._filter_combo)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Поиск по всей базе...")
        self._search_input.setClearButtonEnabled(True)
        self._search_input.setFixedHeight(26)
        self._search_input.setMinimumWidth(200)
        self._search_input.setMaximumWidth(340)
        self._search_input.textChanged.connect(self._on_search)
        bar.addWidget(self._search_input)
        layout.addLayout(bar)

        # Таблица
        self._model = ClientTableModel(self)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setSortingEnabled(True)
        self._table.setShowGrid(False)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setMouseTracking(True)

        header = self._table.horizontalHeader()
        for i, (_, w) in enumerate(_COLUMNS):
            if w == 0:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                self._table.setColumnWidth(i, w)

        self._table.doubleClicked.connect(self._on_double_click)
        layout.addWidget(self._table, stretch=1)

        # Пустое состояние (скрыто по умолчанию)
        self._empty_state = QLabel("📋 Нет клиентов\nДобавьте первого клиента на вкладке «Добавить»")
        self._empty_state.setAlignment(Qt.AlignCenter)
        self._empty_state.setProperty("cssClass", "hint")
        self._empty_state.setStyleSheet(
            "font-size:13px;color:" + theme_engine.colors().text_secondary + ";"
        )
        self._empty_state.setVisible(False)
        layout.addWidget(self._empty_state)

        # Статус
        self._status = QLabel("")
        self._status.setProperty("cssClass", "hint")
        layout.addWidget(self._status)

    # --- Данные ---

    def _apply_filter(self, clients: List[Client]) -> List[Client]:
        """Filter clients by completion status combo box."""
        idx = self._filter_combo.currentIndex()
        if idx == 1:  # Выполненные
            return [c for c in clients if c.is_completed]
        if idx == 2:  # В ожидании
            return [c for c in clients if not c.is_completed]
        return clients

    def refresh(self, clients: Optional[List[Client]] = None) -> None:
        try:
            if clients is None:
                clients = self.db.get_all_clients()
            clients = self._apply_filter(clients or [])
            self._model.set_clients(clients)
            n = len(clients)
            self._table.setVisible(n > 0)
            self._empty_state.setVisible(n == 0)
            self._status.setText(f"Всего: {n}" if n else "")
        except Exception as e:
            logger.error("Ошибка загрузки клиентов: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")

    # --- Поиск ---

    def _on_search(self, text: str) -> None:
        if len(text.strip()) < 2:
            self._search_timer.stop()
            self.refresh()
            return
        self._search_timer.start(300)

    def _do_search(self) -> None:
        q = self._search_input.text().strip()
        if len(q) < 2:
            self.refresh()
            return
        try:
            self.refresh(self.db.search_clients(q))
        except Exception as e:
            logger.error("Ошибка поиска: %s", e)

    def _clear_search(self) -> None:
        self._search_input.clear()
        self._filter_combo.setCurrentIndex(0)
        self.refresh()

    def focus_search(self) -> None:
        self._search_input.setFocus()
        self._search_input.selectAll()

    # --- Выбор ---

    def _selected_client(self) -> Optional[Client]:
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            self.notifier.show_warning("Выберите клиента")
            return None
        return self._model.client_at(rows[0].row())

    # --- Действия ---

    def edit_selected(self) -> None:
        client = self._selected_client()
        if not client:
            return
        from gui_qt.dialogs.edit_client_dialog import EditClientDialog
        if EditClientDialog(self.window(), self.db, client.id, self.notifier).exec():
            self.refresh()
            self.refresh_callback()

    def delete_selected(self) -> None:
        client = self._selected_client()
        if not client:
            return
        if ConfirmDialog.confirm(self, "Подтверждение", f"Удалить '{client.name}'?"):
            self.db.delete_client(client.id)
            self.refresh()
            self.refresh_callback()

    def toggle_completed(self) -> None:
        client = self._selected_client()
        if not client:
            return
        self.db.toggle_completed(client.id)
        self.refresh()
        self.refresh_callback()

    def _on_double_click(self, index: QModelIndex) -> None:
        client = self._model.client_at(index.row())
        if client and client.telegram and client.telegram != "—":
            QApplication.clipboard().setText(client.telegram)
            self.notifier.show_success(f"Скопировано: {client.telegram}")
