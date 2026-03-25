# -*- coding: utf-8 -*-

"""Фрейм настроек / выбора темы — карточки с превью цветов."""
import logging
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
    "amethyst": "💜 Аметистовая", "midnight": "🌙 Полуночная", "sunrise": "🌅 Рассветная",
}

_PREVIEW: Dict[str, list] = {
    "emerald": ["#2e7d32", "#388e3c", "#f5f9f5", "#66bb6a"],
    "sapphire": ["#1565c0", "#1976d2", "#f4f7fb", "#42a5f5"],
    "ruby": ["#c62828", "#d32f2f", "#fdf5f5", "#ef5350"],
    "amethyst": ["#6a1b9a", "#7b1fa2", "#f8f4fb", "#ab47bc"],
    "midnight": ["#82b1ff", "#448aff", "#181c24", "#e0e6ef"],
    "sunrise": ["#ef6c00", "#f57c00", "#fffaf4", "#ffa726"],
}


class ThemeCard(QFrame):
    """Карточка темы — компактная."""

    def __init__(self, key: str, name: str, colors: list,
                 on_click: Callable, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(90)
        tc = theme_engine.colors()
        self.setStyleSheet(
            f"QFrame{{border:1px solid {tc.border};border-radius:10px;"
            f"background:{tc.background_secondary};}}"
            f"QFrame:hover{{border:2px solid {colors[0]};}}"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(3)

        strip = QFrame()
        strip.setFixedHeight(4)
        strip.setStyleSheet(f"background:{colors[0]};border-radius:2px;border:none;")
        layout.addWidget(strip)

        nl = QLabel(name)
        nl.setStyleSheet(
            f"font-size:12px;font-weight:700;border:none;"
            f"color:{tc.text_primary};background:transparent;"
        )
        layout.addWidget(nl)

        dots = QHBoxLayout()
        dots.setSpacing(4)
        for c in colors[:4]:
            dot = QFrame()
            dot.setFixedSize(16, 16)
            dot.setStyleSheet(
                f"background:{c};border-radius:4px;border:1px solid {tc.border};"
            )
            dots.addWidget(dot)
        dots.addStretch()

        sb = QPushButton("Выбрать")
        sb.setFixedSize(65, 24)
        sb.setStyleSheet(
            f"QPushButton{{background:{colors[0]};color:white;"
            f"border-radius:5px;font-size:9px;font-weight:600;border:none;}}"
            f"QPushButton:hover{{opacity:0.85;}}"
        )
        sb.clicked.connect(lambda: on_click(key))
        dots.addWidget(sb)
        layout.addLayout(dots)


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

        # Сетка карточек
        grid = QGridLayout()
        grid.setSpacing(10)
        for i, (key, _) in enumerate(theme_engine.get_all_themes().items()):
            name = _NAMES.get(key, key.capitalize())
            colors = _PREVIEW.get(key, ["#888", "#999", "#eee", "#bbb"])
            grid.addWidget(ThemeCard(key, name, colors, self._apply), i // 3, i % 3)
        layout.addLayout(grid, stretch=1)

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
