# -*- coding: utf-8 -*-

"""
Splash Screen — отображается при запуске приложения
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QWidget,
)


class SplashScreen(QSplashScreen):
    """Красивый splash screen при запуске"""

    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(420, 260)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Контейнер
        container = QWidget(self)
        container.setGeometry(0, 0, 420, 260)
        container.setStyleSheet(
            "background-color: #1a2332; border-radius: 12px;"
        )

        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(10)

        # Заголовок
        title = QLabel("СИСТЕМА УПРАВЛЕНИЯ\nКЛИЕНТАМИ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0; background: transparent;")
        layout.addWidget(title)

        # Версия
        from version import VERSION
        version = QLabel(f"v{VERSION}")
        version.setAlignment(Qt.AlignCenter)
        version.setFont(QFont("Segoe UI", 11))
        version.setStyleSheet("color: #64b5f6; background: transparent;")
        layout.addWidget(version)

        layout.addSpacing(10)

        # Прогресс-бар
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(6)
        self._progress.setStyleSheet("""
            QProgressBar {
                background-color: #2a3a4a;
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #64b5f6;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self._progress)

        # Статус
        self._status = QLabel("Инициализация...")
        self._status.setAlignment(Qt.AlignCenter)
        self._status.setFont(QFont("Segoe UI", 9))
        self._status.setStyleSheet("color: #90a4ae; background: transparent;")
        layout.addWidget(self._status)

        # Автор
        author = QLabel("by kScrewdze")
        author.setAlignment(Qt.AlignCenter)
        author.setFont(QFont("Segoe UI", 8))
        author.setStyleSheet("color: #546e7a; background: transparent;")
        layout.addWidget(author)

    def set_progress(self, value: int, text: str = "") -> None:
        """Обновить прогресс и текст статуса."""
        self._progress.setValue(value)
        if text:
            self._status.setText(text)
        # Важно: обработать события чтобы UI обновился
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
