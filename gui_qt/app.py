# -*- coding: utf-8 -*-

"""
Точка входа PySide6-приложения.
Создаёт QApplication, показывает splash screen, запускает MainWindow.
"""
import sys
import logging

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon

logger = logging.getLogger(__name__)


def run_app() -> None:
    """Запустить приложение с splash screen."""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    from version import VERSION
    app.setApplicationName("Управление клиентами")
    app.setApplicationVersion(VERSION)

    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    # Window icon (taskbar + title bar)
    import os
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icon.ico")
    if getattr(sys, "frozen", False):
        # --onedir: data files in _MEIPASS (_internal/), fallback to exe dir
        meipass = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        icon_path = os.path.join(meipass, "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(sys.executable), "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Splash
    from gui_qt.splash import SplashScreen
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    splash.set_progress(10, "Загрузка модулей...")

    from gui_qt.theme import theme_engine
    app.setStyleSheet(theme_engine.generate_qss())

    splash.set_progress(30, "Инициализация базы данных...")

    from gui_qt.main_window import MainWindow
    splash.set_progress(50, "Создание интерфейса...")

    window = MainWindow()

    splash.set_progress(80, "Загрузка данных...")
    window.refresh_data()
    splash.set_progress(100, "Готово!")

    QTimer.singleShot(300, lambda: _finish(splash, window))
    sys.exit(app.exec())


def _finish(splash, window) -> None:
    splash.close()
    window.show()
