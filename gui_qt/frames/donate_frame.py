# -*- coding: utf-8 -*-

"""Фрейм благодарности автору — ссылки на донат."""
import logging
import webbrowser
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QSizePolicy,
)

from gui_qt.theme import theme_engine

logger = logging.getLogger(__name__)

_DONATE_URL = "https://www.donationalerts.com/r/kscrewdze"


class _DonateCard(QFrame):
    """Карточка способа поддержки."""

    def __init__(self, emoji: str, title: str, description: str,
                 btn_text: str, url: str, color: str,
                 highlighted: bool = False,
                 parent: QWidget = None) -> None:
        super().__init__(parent)
        self._url = url
        tc = theme_engine.colors()
        self.setProperty("cssClass", "card")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumWidth(220)
        self.setMaximumWidth(340)

        if highlighted:
            self.setStyleSheet(
                f"_DonateCard{{"
                f"  background:{tc.background_secondary};"
                f"  border:2px solid {color};"
                f"  border-radius:12px;"
                f"}}"
            )

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        # Цветная полоска сверху
        stripe = QFrame()
        stripe.setFixedHeight(6 if highlighted else 4)
        stripe.setStyleSheet(
            f"border:none;border-radius:3px;background:{color};"
        )
        layout.addWidget(stripe)

        icon = QLabel(emoji)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(
            f"font-size:{'52' if highlighted else '40'}px;"
            "border:none;background:transparent;"
        )
        layout.addWidget(icon)

        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet(
            f"font-size:{'16' if highlighted else '14'}px;font-weight:700;"
            f"color:{tc.text_primary};border:none;background:transparent;"
        )
        layout.addWidget(title_lbl)

        desc = QLabel(description)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet(
            f"font-size:11px;color:{tc.text_secondary};"
            "border:none;background:transparent;"
        )
        layout.addWidget(desc)

        layout.addSpacing(4)

        btn = QPushButton(btn_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(38 if highlighted else 32)
        if highlighted:
            btn.setStyleSheet(
                f"QPushButton{{background:{color};color:#fff;border:none;"
                f"border-radius:8px;font-weight:700;font-size:14px;padding:0 24px;}}"
                f"QPushButton:hover{{background:{color};border:2px solid #fff;}}"
            )
        else:
            btn.setStyleSheet(
                f"QPushButton{{background:{color};color:#fff;border:none;"
                f"border-radius:6px;font-weight:600;font-size:12px;padding:0 16px;}}"
                f"QPushButton:hover{{opacity:0.85;}}"
            )
        btn.clicked.connect(self._open)
        layout.addWidget(btn)

    def _open(self) -> None:
        try:
            webbrowser.open(self._url)
        except Exception as e:
            logger.error("Failed to open URL: %s", e)


class DonateFrame(QWidget):
    """Фрейм поддержки автора."""

    def __init__(self, notifier: Any) -> None:
        super().__init__()
        self.notifier = notifier
        self._create_widgets()

    def _create_widgets(self) -> None:
        tc = theme_engine.colors()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Заголовок
        title = QLabel("ПОДДЕРЖАТЬ ПРОЕКТ")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Если приложение оказалось полезным — вы можете поддержать автора.\n"
            "Это мотивирует продолжать разработку и добавлять новые функции ❤️"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            f"font-size:12px;color:{tc.text_secondary};padding:0 40px;"
        )
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        # Карточки
        cards = QHBoxLayout()
        cards.setSpacing(16)
        cards.setAlignment(Qt.AlignCenter)

        cards.addWidget(_DonateCard(
            emoji="☕",
            title="Купить кофе",
            description="Небольшой донат — уже большая поддержка!\n"
                        "Угостите разработчика чашечкой кофе ☕",
            btn_text="Поддержать ☕",
            url=_DONATE_URL,
            color="#e8a317",
            highlighted=True,
        ))

        cards.addWidget(_DonateCard(
            emoji="⭐",
            title="Звезда на GitHub",
            description="Бесплатный способ сказать «спасибо» — "
                        "поставьте звезду репозиторию.",
            btn_text="GitHub ⭐",
            url="https://github.com/kscrewdze/client-management-system",
            color=tc.accent if hasattr(tc, "accent") else "#6366f1",
        ))

        cards.addWidget(_DonateCard(
            emoji="✈️",
            title="Написать в Telegram",
            description="Хотите новую тему, фичу или нашли баг?\n"
                        "Напишите мне напрямую в Telegram!",
            btn_text="@kscrewdze",
            url="https://t.me/kscrewdze",
            color="#2AABEE",
            highlighted=True,
        ))

        layout.addLayout(cards)

        layout.addStretch()

        # Подвал
        from version import VERSION
        footer = QLabel(f"Сделано с ❤️ by kScrewdze  •  v{VERSION}")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(
            f"font-size:10px;color:{tc.text_secondary};"
        )
        layout.addWidget(footer)
