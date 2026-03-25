# -*- coding: utf-8 -*-

"""Фрейм статистики — компактные карточки с показателями."""
import logging
from typing import Any, Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QFrame,
)

from gui_qt.helpers import fmt_price
from gui_qt.theme import theme_engine

logger = logging.getLogger(__name__)

# Маппинг карточек на цветовое поле ThemeColors и эмодзи
_CARD_DEFS = [
    ("Всего клиентов", "total_clients", "primary", "👥"),
    ("Общий заработок", "total_earnings", "success", "💰"),
    ("Средний чек", "average_price", "warning", "📊"),
    ("Выполнено", "completed_count", "info", "✅"),
    ("Заработано (вып.)", "completed_earnings", "accent", "🎯"),
    ("Матриц", "matrices_count", "secondary", "📐"),
]


class StatCard(QFrame):
    """Одна карточка статистики с цветом из темы."""

    def __init__(self, title: str, emoji: str, color_key: str, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._color_key = color_key
        self.setMinimumHeight(80)
        self.setProperty("cssClass", "card")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        # Иконка + Заголовок в строку
        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignCenter)
        top_row.setSpacing(4)

        icon_lbl = QLabel(emoji)
        icon_lbl.setStyleSheet("font-size:14px;background:transparent;border:none;")
        top_row.addWidget(icon_lbl)

        self._title = QLabel(title)
        self._title.setAlignment(Qt.AlignCenter)
        self._title.setProperty("cssClass", "hint")
        top_row.addWidget(self._title)
        layout.addLayout(top_row)

        self._value = QLabel("0")
        self._value.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._value)

        # Цветная полоска снизу
        self._stripe = QFrame()
        self._stripe.setFixedHeight(3)
        self._stripe.setStyleSheet("border:none;border-radius:1px;")
        layout.addWidget(self._stripe)

        self._apply_theme_color()

    def _apply_theme_color(self) -> None:
        """Применить цвет из текущей темы."""
        c = theme_engine.colors()
        color = getattr(c, self._color_key, c.primary)
        self._value.setStyleSheet(
            f"font-size:20px;font-weight:700;color:{color};"
            f"background:transparent;border:none;"
        )
        self._stripe.setStyleSheet(
            f"background:{color};border:none;border-radius:1px;"
        )

    def set_value(self, text: str) -> None:
        self._value.setText(text)

    def refresh_theme(self) -> None:
        """Обновить цвета при смене темы."""
        self._apply_theme_color()


class StatisticsFrame(QWidget):
    """Фрейм со статистикой."""

    def __init__(self, db: Any, notifier: Any) -> None:
        super().__init__()
        self.db = db
        self.notifier = notifier
        self._cards: Dict[str, StatCard] = {}
        self._create_widgets()
        self.refresh()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("СТАТИСТИКА")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(8)

        grid = QGridLayout()
        grid.setSpacing(10)

        for i, (t, key, color_key, emoji) in enumerate(_CARD_DEFS):
            card = StatCard(t, emoji, color_key)
            grid.addWidget(card, i // 3, i % 3)
            self._cards[key] = card

        layout.addLayout(grid, stretch=1)

    def refresh(self) -> None:
        try:
            s = self.db.get_statistics()
            self._cards["total_clients"].set_value(str(s["total_clients"]))
            self._cards["total_earnings"].set_value(fmt_price(s["total_earnings"]))
            self._cards["average_price"].set_value(fmt_price(s["average_price"]))
            self._cards["completed_count"].set_value(str(s["completed_count"]))
            self._cards["completed_earnings"].set_value(fmt_price(s["completed_earnings"]))
            self._cards["matrices_count"].set_value(str(s["matrices_count"]))
            # Обновить цвета (на случай смены темы)
            for card in self._cards.values():
                card.refresh_theme()
        except Exception as e:
            logger.error("Ошибка статистики: %s", e)
            self.notifier.show_error(f"Ошибка: {e}")
