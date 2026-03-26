# -*- coding: utf-8 -*-

"""Фрейм настроек / выбора темы — карточки с превью цветов."""
import logging
import webbrowser
from typing import Any, Callable, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton,
)

from gui_qt.theme import theme_engine

logger = logging.getLogger(__name__)

_NAMES: Dict[str, str] = {
    "emerald": "🌿 Изумрудная", "sapphire": "💎 Сапфировая", "ruby": "❤️ Рубиновая",
    "amethyst": "💜 Аметистовая", "dark": "🖤 Тёмная", "glass": "🪟 Стеклянная",
}

_PREVIEW: Dict[str, list] = {
    "emerald": ["#2e7d32", "#388e3c", "#f5f9f5", "#66bb6a"],
    "sapphire": ["#1565c0", "#1976d2", "#f4f7fb", "#42a5f5"],
    "ruby": ["#c62828", "#d32f2f", "#fdf5f5", "#ef5350"],
    "amethyst": ["#6a1b9a", "#7b1fa2", "#f8f4fb", "#ab47bc"],
    "dark": ["#bb86fc", "#985eff", "#121212", "#e1e1e1"],
    "glass": ["#5c6bc0", "#7986cb", "#ebf0f5", "#26c6da"],
}


class ThemeCard(QFrame):
    """Карточка темы — компактная."""

    def __init__(self, key: str, name: str, colors: list,
                 on_click: Callable, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(68)
        tc = theme_engine.colors()
        self.setStyleSheet(
            f"QFrame{{border:1px solid {tc.border};border-radius:8px;"
            f"background:{tc.background_secondary};}}"
            f"QFrame:hover{{border:2px solid {colors[0]};}}"
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        # Color dots
        dots_col = QVBoxLayout()
        dots_col.setSpacing(2)
        dots_row = QHBoxLayout()
        dots_row.setSpacing(3)
        for c in colors[:4]:
            dot = QFrame()
            dot.setFixedSize(12, 12)
            dot.setStyleSheet(
                f"background:{c};border-radius:3px;border:1px solid {tc.border};"
            )
            dots_row.addWidget(dot)
        dots_col.addLayout(dots_row)
        layout.addLayout(dots_col)

        # Name
        nl = QLabel(name)
        nl.setStyleSheet(
            f"font-size:11px;font-weight:700;border:none;"
            f"color:{tc.text_primary};background:transparent;"
        )
        layout.addWidget(nl, stretch=1)

        # Button
        sb = QPushButton("Выбрать")
        sb.setFixedSize(60, 22)
        sb.setStyleSheet(
            f"QPushButton{{background:{colors[0]};color:white;"
            f"border-radius:4px;font-size:9px;font-weight:600;border:none;}}"
            f"QPushButton:hover{{opacity:0.85;}}"
        )
        sb.clicked.connect(lambda: on_click(key))
        layout.addWidget(sb)


class SettingsFrame(QWidget):
    """Фрейм выбора темы."""

    def __init__(self, notifier: Any, on_theme_applied: Callable) -> None:
        super().__init__()
        self.notifier = notifier
        self._on_theme_applied = on_theme_applied
        self._current_label: Optional[QLabel] = None
        self._create_widgets()

    def _create_widgets(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        title = QLabel("ВЫБОР ТЕМЫ")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текущая тема
        cr = QHBoxLayout()
        cr.addStretch()
        current_prefix = QLabel("Текущая тема:")
        current_prefix.setProperty("cssClass", "hint")
        cr.addWidget(current_prefix)
        current = theme_engine.get_current_theme()
        current_key = self._get_theme_key(current)
        self._current_label = QLabel(_NAMES.get(current_key, current.name if current else "Стандартная"))
        self._current_label.setProperty("cssClass", "subtitle")
        cr.addWidget(self._current_label)
        cr.addStretch()
        layout.addLayout(cr)

        layout.addSpacing(4)

        # Сетка карточек (2 колонки)
        grid = QGridLayout()
        grid.setSpacing(8)
        for i, (key, _) in enumerate(theme_engine.get_all_themes().items()):
            name = _NAMES.get(key, key.capitalize())
            colors = _PREVIEW.get(key, ["#888", "#999", "#eee", "#bbb"])
            grid.addWidget(ThemeCard(key, name, colors, self._apply), i // 2, i % 2)
        layout.addLayout(grid)

        layout.addSpacing(8)

        # "Предложить тему" button
        suggest_row = QHBoxLayout()
        suggest_row.addStretch()
        suggest_btn = QPushButton("✨ Предложить тему")
        suggest_btn.setCursor(Qt.PointingHandCursor)
        suggest_btn.setFixedHeight(32)
        suggest_btn.setMinimumWidth(180)
        tc = theme_engine.colors()
        suggest_btn.setStyleSheet(
            f"QPushButton{{background:transparent;color:{tc.primary};"
            f"border:2px solid {tc.primary};border-radius:8px;"
            f"font-size:12px;font-weight:600;padding:0 20px;}}"
            f"QPushButton:hover{{background:{tc.primary};color:{tc.text_inverse};}}"
        )
        suggest_btn.clicked.connect(
            lambda: webbrowser.open("https://t.me/kscrewdze")
        )
        suggest_row.addWidget(suggest_btn)
        suggest_row.addStretch()
        layout.addLayout(suggest_row)

        layout.addStretch()

    def _apply(self, key: str) -> None:
        if theme_engine.apply_theme(key):
            name = _NAMES.get(key, key)
            self._current_label.setText(name)
            self._on_theme_applied()
            self.notifier.show_success(f"Тема '{name}' применена")

    def _get_theme_key(self, theme) -> str:
        """Получить ключ темы по объекту."""
        if not theme:
            return ""
        for key, t in theme_engine.themes.items():
            if t is theme:
                return key
        return ""

    def refresh(self) -> None:
        current = theme_engine.get_current_theme()
        if current and self._current_label:
            key = self._get_theme_key(current)
            self._current_label.setText(_NAMES.get(key, current.name))
