# -*- coding: utf-8 -*-

"""Фрейм клиентов — QTableView + поиск + CRUD (компактный)."""
import logging
from typing import Any, Callable, List, Optional

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTableView, QHeaderView,
    QAbstractItemView, QApplication,
)

from database.models import Client
from gui_qt.helpers import fmt_price
from gui_qt.theme import theme_engine
from gui_qt.widgets import ConfirmDialog

logger = logging.getLogger(__name__)

_COLUMNS = [
    ("", 30), ("Имя", 0), ("Telegram", 110), ("Телефон", 110),
    ("Дата рожд.", 80), ("ЧС", 32), ("Матрица", 140),
    ("Цена", 75), ("Дата заказа", 80),
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
                c.matrix_name or "—",
                fmt_price(c.service_price),
                c.order_date,
            ][col]

        if role == Qt.TextAlignmentRole:
            if col in (0, 4, 5, 8):
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
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Верхняя строка: заголовок + поиск
        top = QHBoxLayout()
        top.setSpacing(8)
        title = QLabel("КЛИЕНТЫ")
        title.setProperty("cssClass", "title")
        top.addWidget(title)
        top.addStretch()

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("🔍 Поиск по имени, телефону, Telegram...")
        self._search_input.setFixedWidth(280)
        self._search_input.setFixedHeight(28)
        self._search_input.textChanged.connect(self._on_search)
        top.addWidget(self._search_input)

        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(28, 28)
        clear_btn.setProperty("cssClass", "flat")
        clear_btn.setToolTip("Очистить поиск")
        clear_btn.clicked.connect(self._clear_search)
        top.addWidget(clear_btn)
        layout.addLayout(top)

        # Кнопки действий
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        for text, cls, handler, tooltip in [
            ("🔄 Обновить", "info", lambda: self.refresh(), "Обновить список (Ctrl+R)"),
            ("✏️ Редактировать", "warning", self.edit_selected, "Редактировать клиента (Ctrl+E)"),
            ("🗑 Удалить", "danger", self.delete_selected, "Удалить клиента (Ctrl+D)"),
            ("✔ Отметить", "success", self.toggle_completed, "Отметить как выполнен"),
        ]:
            b = QPushButton(text)
            b.setProperty("cssClass", cls)
            b.setFixedHeight(28)
            b.setToolTip(tooltip)
            b.clicked.connect(handler)
            btn_row.addWidget(b)

        btn_row.addStretch()
        hint = QLabel("💡 Двойной клик — копировать Telegram")
        hint.setProperty("cssClass", "hint")
        btn_row.addWidget(hint)
        layout.addLayout(btn_row)

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

    def refresh(self, clients: Optional[List[Client]] = None) -> None:
        try:
            if clients is None:
                clients = self.db.get_all_clients()
            self._model.set_clients(clients or [])
            n = len(clients) if clients else 0
            self._table.setVisible(n > 0)
            self._empty_state.setVisible(n == 0)
            self._status.setText(f"Всего клиентов: {n}" if n else "")
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
