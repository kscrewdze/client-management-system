# -*- coding: utf-8 -*-

"""
Виджеты общего назначения: уведомления (Toast), подтверждение
"""
import logging
from typing import Optional

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtWidgets import (
    QLabel, QHBoxLayout, QWidget, QGraphicsOpacityEffect,
    QDialog, QVBoxLayout, QPushButton, QMessageBox,
)

logger = logging.getLogger(__name__)


# ======================================================================
# Toast-уведомления
# ======================================================================

class ToastNotification(QLabel):
    """Плавающее уведомление (toast) с fade-анимацией"""

    _ICON_MAP = {
        "success": "✅",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️",
    }

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setFixedHeight(44)
        self.setMinimumWidth(280)
        self.hide()

        # Анимация прозрачности
        self._opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity)
        self._opacity.setOpacity(0.0)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._fade_out)

        self._anim: Optional[QPropertyAnimation] = None

    # ---- Публичные методы ----

    def show_message(self, text: str, color: str = "#2e7d32",
                     duration: int = 2500, kind: str = "info") -> None:
        """Показать уведомление с цветом и длительностью в мс."""
        icon = self._ICON_MAP.get(kind, "")
        display = f"{icon} {text}" if icon else text
        self.setText(display)
        self.setStyleSheet(
            f"background-color: {color}; color: white; "
            f"border-radius: 10px; padding: 8px 24px; "
            f"font-family: 'Segoe UI'; font-size: 12px; font-weight: bold;"
        )
        self._reposition()
        self.show()
        self.raise_()
        self._fade_in()
        self._timer.start(duration)

    def show_success(self, text: str) -> None:
        self.show_message(text, "#2e7d32", 2000, "success")

    def show_error(self, text: str) -> None:
        self.show_message(text, "#d32f2f", 3500, "error")

    def show_info(self, text: str) -> None:
        self.show_message(text, "#0288d1", 2000, "info")

    def show_warning(self, text: str) -> None:
        self.show_message(text, "#ed6c02", 2500, "warning")

    # ---- Внутренние ----

    def _reposition(self) -> None:
        """Позиционировать по центру верхней части родителя."""
        p = self.parent()
        if p:
            self.adjustSize()
            w = max(self.sizeHint().width(), 280)
            w = min(w, p.width() - 40)  # Не шире родителя за вычетом отступов
            self.setFixedWidth(w)
            x = (p.width() - w) // 2
            self.move(x, 50)

    def _fade_in(self) -> None:
        self._stop_anim()
        self._opacity.setOpacity(1.0)
        self._anim = QPropertyAnimation(self._opacity, b"opacity")
        self._anim.setDuration(200)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def _fade_out(self) -> None:
        self._stop_anim()
        self._anim = QPropertyAnimation(self._opacity, b"opacity")
        self._anim.setDuration(400)
        self._anim.setStartValue(self._opacity.opacity())
        self._anim.setEndValue(0.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.finished.connect(self._on_fade_out_done)
        self._anim.start()

    def _on_fade_out_done(self) -> None:
        self.hide()
        self._opacity.setOpacity(0.0)

    def _stop_anim(self) -> None:
        if self._anim:
            self._anim.finished.disconnect()
            if self._anim.state() == QPropertyAnimation.Running:
                self._anim.stop()
            self._anim = None


# ======================================================================
# Диалог подтверждения (замена tkinter messagebox)
# ======================================================================

class ConfirmDialog(QDialog):
    """Стилизованный диалог подтверждения."""

    def __init__(
        self,
        parent: QWidget,
        title: str = "Подтверждение",
        message: str = "Вы уверены?",
        ok_text: str = "OK",
        cancel_text: str = "Отмена",
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(380, 160)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 22, 28, 22)

        msg = QLabel(message)
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("font-size: 13px;")
        layout.addWidget(msg)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(14)

        cancel_btn = QPushButton(cancel_text)
        cancel_btn.setProperty("cssClass", "flat")
        cancel_btn.setFixedHeight(34)
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        ok_btn = QPushButton(ok_text)
        ok_btn.setProperty("cssClass", "danger")
        ok_btn.setFixedHeight(34)
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        btn_row.addWidget(ok_btn)

        layout.addLayout(btn_row)

    @staticmethod
    def confirm(parent: QWidget, title: str, message: str) -> bool:
        """Удобный статический метод — возвращает True/False."""
        dlg = ConfirmDialog(parent, title, message)
        return dlg.exec() == QDialog.Accepted
