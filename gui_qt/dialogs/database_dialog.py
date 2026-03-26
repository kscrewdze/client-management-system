# -*- coding: utf-8 -*-

"""Database Browser dialog — opens DatabaseFrame in a floating window (Ctrl+B)."""

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout

from gui_qt.frames.database_frame import DatabaseFrame


class DatabaseDialog(QDialog):
    """Floating database browser window."""

    def __init__(self, db: Any, notifier: Any, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("🗄 База данных — SQL Browser")
        self.setMinimumSize(900, 500)
        self.resize(1100, 600)
        self.setWindowFlags(
            Qt.Dialog | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._frame = DatabaseFrame(db, notifier)
        layout.addWidget(self._frame)
