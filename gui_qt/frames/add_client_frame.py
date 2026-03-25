# -*- coding: utf-8 -*-

"""Фрейм добавления клиента — использует общие helpers."""
import logging
from typing import Any, Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
    QLabel, QLineEdit, QComboBox, QPushButton, QSizePolicy,
)
from PySide6.QtGui import QKeySequence, QShortcut

from gui_qt.helpers import (
    build_client_form, load_matrices_combo, on_matrix_selected,
    validate_client_form, fmt_price, update_destiny_display,
)

logger = logging.getLogger(__name__)


class AddClientFrame(QWidget):
    """Фрейм для добавления нового клиента."""

    def __init__(self, db: Any, notifier: Any, refresh_callback: Callable) -> None:
        super().__init__()
        self.db = db
        self.notifier = notifier
        self.refresh_callback = refresh_callback
        self._matrix_map = {}
        self._create_widgets()
        self._bind_shortcuts()
        self.refresh()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Заголовок
        title = QLabel("ДОБАВЛЕНИЕ КЛИЕНТА")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        hint = QLabel("Ctrl+Enter — сохранить  │  Ctrl+Q — очистить  │  * — обязательные поля")
        hint.setProperty("cssClass", "hint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        # Форма в карточке
        form_frame = QFrame()
        form_frame.setProperty("cssClass", "card")
        form_outer = QVBoxLayout(form_frame)
        form_outer.setContentsMargins(0, 10, 0, 10)

        # Центрированный grid с макс. шириной
        center_row = QHBoxLayout()
        center_row.addStretch(1)

        grid_widget = QWidget()
        grid_widget.setMaximumWidth(560)
        grid = QGridLayout(grid_widget)
        grid.setContentsMargins(24, 0, 24, 0)
        grid.setVerticalSpacing(8)
        grid.setHorizontalSpacing(12)
        grid.setColumnStretch(1, 1)

        self._entries, self._matrix_combo, self._price_entry, self._destiny_lbl, self._custom_name, _ = (
            build_client_form(grid)
        )
        self._matrix_combo.currentTextChanged.connect(self._on_matrix)
        self._entries["birth_date"].textChanged.connect(self._on_birth_date)

        center_row.addWidget(grid_widget)
        center_row.addStretch(1)
        form_outer.addLayout(center_row)
        layout.addWidget(form_frame, stretch=1)

        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_row.addStretch()
        save_btn = QPushButton("💾 Сохранить (Ctrl+Enter)")
        save_btn.setProperty("cssClass", "success")
        save_btn.setFixedSize(190, 32)
        save_btn.clicked.connect(self.save_client)
        btn_row.addWidget(save_btn)

        clear_btn = QPushButton("🧹 Очистить (Ctrl+Q)")
        clear_btn.setProperty("cssClass", "warning")
        clear_btn.setFixedSize(170, 32)
        clear_btn.clicked.connect(self.clear_form)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._entries["name"].setFocus()

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(self.save_client)
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.clear_form)

    # --- Матрицы ---

    def _on_matrix(self, text: str) -> None:
        on_matrix_selected(text, self._matrix_map, self._price_entry, self._custom_name)

    def _on_birth_date(self, text: str) -> None:
        update_destiny_display(text, self._destiny_lbl)

    def refresh(self) -> None:
        try:
            self._matrix_map = load_matrices_combo(self.db, self._matrix_combo)
        except Exception as e:
            logger.error("Ошибка загрузки матриц: %s", e)

    # --- Сохранение ---

    def save_client(self) -> None:
        data = validate_client_form(
            self._entries, self._price_entry,
            self._matrix_combo.currentText(), self.notifier,
        )
        if not data:
            return

        # Определяем матрицу
        text = self._matrix_combo.currentText()
        info = self._matrix_map.get(text)
        if info:
            matrix_name = info[0]
            matrix_id = info[1]
        else:
            custom = self._custom_name.text().strip()
            matrix_name = custom if custom else "Свой выбор"
            matrix_id = None

        try:
            bd = data["birth_date"].strftime("%d.%m.%Y")
            destiny = self.db.calculate_destiny_number(bd)
            client_data = {
                "name": data["name"],
                "telegram": data["telegram"],
                "phone": data["phone"],
                "birth_date": bd,
                "order_date": data["order_date"].strftime("%d.%m.%Y"),
                "service_name": matrix_name,
                "service_price": data["price"],
                "comment": data["comment"],
                "matrix_id": matrix_id,
                "destiny_number": destiny,
            }
            self.db.add_client(client_data)
            self.notifier.show_success(f"Клиент {data['name']} добавлен!")
            self.clear_form()
            self.refresh_callback()
        except Exception as e:
            logger.error("Ошибка сохранения клиента: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")

    def clear_form(self) -> None:
        for entry in self._entries.values():
            entry.clear()
        self._price_entry.clear()
        self._custom_name.clear()
        self._matrix_combo.setCurrentIndex(0)
        self._entries["name"].setFocus()
