# -*- coding: utf-8 -*-

"""Фрейм экспорта — кнопки для открытия/обновления таблиц Excel."""
import logging
import os
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QSizePolicy,
)

from config.settings import Settings
from gui_qt.theme import theme_engine

logger = logging.getLogger(__name__)


class _ExportCard(QFrame):
    """Карточка экспорта (одна таблица) — цвета из темы."""

    def __init__(self, title: str, filename: str, color_key: str,
                 emoji: str, on_export, on_open, parent=None) -> None:
        super().__init__(parent)
        self._color_key = color_key
        self.setProperty("cssClass", "card")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumWidth(200)
        self.setMaximumWidth(300)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        # Цветная полоска сверху
        self._stripe = QFrame()
        self._stripe.setFixedHeight(4)
        self._stripe.setStyleSheet("border:none;border-radius:2px;")
        layout.addWidget(self._stripe)

        icon = QLabel(emoji)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size:36px;border:none;background:transparent;")
        layout.addWidget(icon)

        self._title_lbl = QLabel(title)
        self._title_lbl.setAlignment(Qt.AlignCenter)
        self._title_lbl.setStyleSheet("font-size:14px;font-weight:700;border:none;background:transparent;")
        layout.addWidget(self._title_lbl)

        f = QLabel(filename)
        f.setAlignment(Qt.AlignCenter)
        f.setProperty("cssClass", "hint")
        layout.addWidget(f)

        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignCenter)
        self._status.setProperty("cssClass", "hint")
        layout.addWidget(self._status)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self._re_btn = QPushButton("🔄 Обновить")
        self._re_btn.setFixedHeight(30)
        self._re_btn.clicked.connect(on_export)
        btn_row.addWidget(self._re_btn)

        self._open_btn = QPushButton("📂 Открыть")
        self._open_btn.setFixedHeight(30)
        self._open_btn.setProperty("cssClass", "flat")
        self._open_btn.clicked.connect(on_open)
        btn_row.addWidget(self._open_btn)

        layout.addLayout(btn_row)

        self._apply_theme_color()

    def _apply_theme_color(self) -> None:
        """Применить цвет из текущей темы."""
        c = theme_engine.colors()
        color = getattr(c, self._color_key, c.primary)
        self._stripe.setStyleSheet(
            f"background:{color};border:none;border-radius:2px;"
        )
        self._title_lbl.setStyleSheet(
            f"font-size:14px;font-weight:700;color:{color};"
            f"border:none;background:transparent;"
        )
        self._re_btn.setStyleSheet(
            f"QPushButton{{background:{color};color:white;border-radius:6px;"
            f"font-weight:600;font-size:11px;border:none;padding:0 14px;}}"
            f"QPushButton:hover{{opacity:0.85;}}"
        )

    def set_status(self, text: str) -> None:
        self._status.setText(text)

    def refresh_theme(self) -> None:
        """Обновить цвета при смене темы."""
        self._apply_theme_color()


class ExportFrame(QWidget):
    """Фрейм экспорта — две карточки: клиенты и матрицы."""

    def __init__(self, db: Any, notifier: Any) -> None:
        super().__init__()
        self.db = db
        self.notifier = notifier
        self._dir = Settings.EXPORTS_DIR
        self._create_widgets()
        self._update_status()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        title = QLabel("ЭКСПОРТ В EXCEL")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        hint = QLabel(
            "Таблицы обновляются автоматически при добавлении, "
            "редактировании или удалении данных"
        )
        hint.setProperty("cssClass", "hint")
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)
        layout.addWidget(hint)

        layout.addStretch(1)

        # Карточки — адаптивная ширина
        cards = QHBoxLayout()
        cards.setSpacing(20)
        cards.addStretch(1)

        self._clients_card = _ExportCard(
            "Клиенты", "clients.xlsx", "primary", "👥",
            self._export_clients, self._open_clients,
        )
        cards.addWidget(self._clients_card)

        self._matrices_card = _ExportCard(
            "Матрицы", "matrices.xlsx", "success", "📐",
            self._export_matrices, self._open_matrices,
        )
        cards.addWidget(self._matrices_card)

        cards.addStretch(1)
        layout.addLayout(cards)

        layout.addStretch(1)

        # Кнопка открытия папки
        folder_row = QHBoxLayout()
        folder_row.addStretch()
        folder_btn = QPushButton("📁 Открыть папку экспорта")
        folder_btn.setProperty("cssClass", "info")
        folder_btn.setFixedHeight(30)
        folder_btn.clicked.connect(self._open_folder)
        folder_row.addWidget(folder_btn)
        folder_row.addStretch()
        layout.addLayout(folder_row)

    def _update_status(self) -> None:
        for name, card in [("clients.xlsx", self._clients_card),
                           ("matrices.xlsx", self._matrices_card)]:
            path = self._dir / name
            if path.exists():
                import datetime
                mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
                card.set_status(f"Обновлено: {mtime.strftime('%d.%m.%Y %H:%M')}")
            else:
                card.set_status("Файл не создан")

    def _export_clients(self) -> None:
        try:
            from gui_qt.exporters import export_clients
            export_clients(self.db)
            self.notifier.show_success("Таблица клиентов обновлена!")
            self._update_status()
        except Exception as e:
            logger.error("Ошибка экспорта клиентов: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")

    def _export_matrices(self) -> None:
        try:
            from gui_qt.exporters import export_matrices
            export_matrices(self.db)
            self.notifier.show_success("Таблица матриц обновлена!")
            self._update_status()
        except Exception as e:
            logger.error("Ошибка экспорта матриц: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")

    def _open_clients(self) -> None:
        self._open_file("clients.xlsx")

    def _open_matrices(self) -> None:
        self._open_file("matrices.xlsx")

    def _open_file(self, name: str) -> None:
        path = self._dir / name
        if not path.exists():
            self.notifier.show_warning(f"Файл {name} не найден. Нажмите «Обновить».")
            return
        try:
            os.startfile(str(path))
        except Exception as e:
            self.notifier.show_error(f"Не удалось открыть: {e}")

    def _open_folder(self) -> None:
        try:
            self._dir.mkdir(exist_ok=True)
            os.startfile(str(self._dir))
        except Exception as e:
            self.notifier.show_error(f"Ошибка: {e}")

    def refresh(self) -> None:
        self._update_status()
        self._clients_card.refresh_theme()
        self._matrices_card.refresh_theme()
