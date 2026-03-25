# -*- coding: utf-8 -*-

"""Диалог редактирования клиента — использует общие helpers."""
import logging
from typing import Any, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
)
from PySide6.QtGui import QKeySequence, QShortcut

from gui_qt.helpers import (
    build_client_form, load_matrices_combo, on_matrix_selected,
    validate_client_form, update_destiny_display,
)

logger = logging.getLogger(__name__)


class EditClientDialog(QDialog):
    """Диалог редактирования клиента."""

    def __init__(self, parent, db: Any, client_id: int, notifier: Any) -> None:
        super().__init__(parent)
        self.db = db
        self.client_id = client_id
        self.notifier = notifier
        self._matrix_map = {}

        self.client = db.get_client_by_id(client_id)
        if not self.client:
            notifier.show_error("Клиент не найден")
            return

        self.setWindowTitle(f"Редактирование: {self.client.name}")
        self.setMinimumSize(480, 400)
        self.setModal(True)

        self._create_ui()
        self._load_data()
        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(self._save)

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        title = QLabel("РЕДАКТИРОВАНИЕ КЛИЕНТА")
        title.setProperty("cssClass", "subtitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        hint = QLabel("Ctrl+Enter — сохранить  │  Esc — отмена")
        hint.setProperty("cssClass", "hint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        layout.addSpacing(4)

        # Форма (общая через helpers)
        grid = QGridLayout()
        grid.setVerticalSpacing(6)
        grid.setHorizontalSpacing(10)
        grid.setColumnStretch(1, 1)

        self._entries, self._matrix_combo, self._price_entry, self._destiny_lbl, self._custom_name, _ = (
            build_client_form(grid)
        )
        self._matrix_combo.currentTextChanged.connect(
            lambda t: on_matrix_selected(t, self._matrix_map, self._price_entry, self._custom_name)
        )
        self._entries["birth_date"].textChanged.connect(
            lambda t: update_destiny_display(t, self._destiny_lbl)
        )
        layout.addLayout(grid, stretch=1)

        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_row.addStretch()
        save_btn = QPushButton("💾 Сохранить")
        save_btn.setProperty("cssClass", "success")
        save_btn.setFixedSize(130, 32)
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setProperty("cssClass", "flat")
        cancel_btn.setFixedSize(90, 32)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _load_data(self) -> None:
        c = self.client
        self._entries["name"].setText(c.name or "")
        self._entries["telegram"].setText(c.telegram or "")
        self._entries["phone"].setText(c.phone or "")
        self._entries["birth_date"].setText(c.birth_date or "")
        self._entries["order_date"].setText(c.order_date or "")
        self._entries["comment"].setText(c.comment or "")

        # Матрицы
        self._matrix_map = load_matrices_combo(
            self.db, self._matrix_combo, add_empty=True,
        )
        # Выбрать текущую матрицу
        found = False
        for i in range(self._matrix_combo.count()):
            info = self._matrix_map.get(self._matrix_combo.itemText(i))
            if info and info[1] == c.matrix_id:
                self._matrix_combo.setCurrentIndex(i)
                found = True
                break
        if not found and c.service_name:
            # Свой выбор — выбираем "Свой выбор" и заполняем название
            for i in range(self._matrix_combo.count()):
                if "Свой выбор" in self._matrix_combo.itemText(i):
                    self._matrix_combo.setCurrentIndex(i)
                    self._custom_name.setText(c.service_name)
                    break
        self._price_entry.setText(str(int(c.service_price)))

    def _save(self) -> None:
        data = validate_client_form(
            self._entries, self._price_entry,
            self._matrix_combo.currentText(), self.notifier,
        )
        if not data:
            return

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
            self.db.update_client(self.client_id, client_data)
            self.notifier.show_success("Данные клиента обновлены!")
            self.accept()
        except Exception as e:
            logger.error("Ошибка сохранения: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")
