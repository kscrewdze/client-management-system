# -*- coding: utf-8 -*-

"""
Диалог добавления / редактирования матрицы
"""
import logging
from typing import Any, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
)
from PySide6.QtGui import QKeySequence, QShortcut

logger = logging.getLogger(__name__)


class MatrixDialog(QDialog):
    """Диалог добавления / редактирования матрицы"""

    def __init__(
        self, parent, notifier: Any,
        matrix_id: Optional[int] = None,
        matrix_data: Optional[Tuple] = None,
    ) -> None:
        super().__init__(parent)
        self.notifier = notifier
        self.matrix_id = matrix_id
        self.result: Optional[Tuple[str, float]] = None

        is_edit = matrix_id is not None
        self.setWindowTitle("Редактирование матрицы" if is_edit else "Добавление матрицы")
        self.setFixedSize(380, 200)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(8)

        # Заголовок
        title = QLabel("РЕДАКТИРОВАНИЕ" if is_edit else "ДОБАВЛЕНИЕ МАТРИЦЫ")
        title.setProperty("cssClass", "subtitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(4)

        # Название
        layout.addWidget(QLabel("Название матрицы:"))
        self._name_entry = QLineEdit()
        self._name_entry.setPlaceholderText("Введите название")
        self._name_entry.setMinimumHeight(28)
        layout.addWidget(self._name_entry)

        # Цена
        layout.addWidget(QLabel("Цена (руб):"))
        self._price_entry = QLineEdit()
        self._price_entry.setPlaceholderText("0")
        self._price_entry.setMinimumHeight(28)
        self._price_entry.setFixedWidth(200)
        layout.addWidget(self._price_entry)

        # Заполняем при редактировании
        if matrix_data:
            self._name_entry.setText(matrix_data[1])
            self._price_entry.setText(str(int(matrix_data[2])))

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

        # Шорткаты
        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(self._save)
        self._name_entry.setFocus()

    def _save(self) -> None:
        name = self._name_entry.text().strip()
        price_str = self._price_entry.text().strip()

        if not name:
            self.notifier.show_error("Введите название матрицы!")
            return
        if not price_str:
            self.notifier.show_error("Введите цену!")
            return

        try:
            price = float(price_str.replace(",", "."))
        except ValueError:
            self.notifier.show_error("Неверный формат цены!")
            return

        self.result = (name, price)
        self.accept()
