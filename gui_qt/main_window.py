# -*- coding: utf-8 -*-

"""
Главное окно — QMainWindow с QTabWidget (7 вкладок).
Компактный header, status bar, keyboard shortcuts.
"""
import logging
import os
from datetime import datetime
from typing import Dict, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QShortcut, QKeySequence, QCloseEvent
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QStatusBar, QFrame,
)

from config.settings import Settings
from database import Database
from gui_qt.theme import theme_engine
from gui_qt.widgets import ToastNotification, ConfirmDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Главное окно приложения."""

    theme_changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(Settings.APP_TITLE)
        self.setMinimumSize(*Settings.APP_MIN_SIZE)
        self.resize(Settings.APP_WIDTH, Settings.APP_HEIGHT)

        Settings.ensure_directories()
        self.db = Database()
        self.notifier = ToastNotification(self)

        central = QWidget()
        self.setCentralWidget(central)
        self._layout = QVBoxLayout(central)
        self._layout.setContentsMargins(6, 6, 6, 6)
        self._layout.setSpacing(3)

        self._create_header()
        self._create_tabs()
        self._create_status_bar()
        self._bind_shortcuts()
        self._apply_current_theme()

        self._clock = QTimer(self)
        self._clock.timeout.connect(self._tick)
        self._clock.start(1000)
        self._center()
        logger.info("MainWindow инициализирован")

    # --- Header ---

    def _create_header(self) -> None:
        hdr = QFrame()
        hdr.setFixedHeight(32)
        hdr.setProperty("cssClass", "transparent")
        h = QHBoxLayout(hdr)
        h.setContentsMargins(10, 2, 10, 2)

        self._title = QLabel("СИСТЕМА УПРАВЛЕНИЯ КЛИЕНТАМИ")
        self._title.setProperty("cssClass", "title")
        h.addWidget(self._title)
        h.addStretch()

        self._clock_lbl = QLabel()
        self._clock_lbl.setProperty("cssClass", "hint")
        h.addWidget(self._clock_lbl)
        self._tick()
        self._layout.addWidget(hdr)

        # Разделитель между хедером и вкладками
        separator = QFrame()
        separator.setProperty("cssClass", "separator")
        self._layout.addWidget(separator)

    def _tick(self) -> None:
        self._clock_lbl.setText(datetime.now().strftime("%d.%m.%Y  %H:%M:%S"))

    # --- Tabs ---

    def _create_tabs(self) -> None:
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        from gui_qt.frames.statistics_frame import StatisticsFrame
        from gui_qt.frames.clients_frame import ClientsFrame
        from gui_qt.frames.add_client_frame import AddClientFrame
        from gui_qt.frames.matrices_frame import MatricesFrame
        from gui_qt.frames.export_frame import ExportFrame
        from gui_qt.frames.settings_frame import SettingsFrame
        from gui_qt.frames.database_frame import DatabaseFrame

        self._frames: Dict[str, QWidget] = {}

        tabs_def = [
            ("statistics", StatisticsFrame(self.db, self.notifier), "📊 Статистика"),
            ("clients", ClientsFrame(self.db, self.notifier, self.refresh_data), "👥 Клиенты"),
            ("matrices", MatricesFrame(self.db, self.notifier, self.refresh_data), "📐 Матрицы"),
            ("add", AddClientFrame(self.db, self.notifier, self.refresh_data), "➕ Добавить"),
            ("export", ExportFrame(self.db, self.notifier), "📤 Экспорт"),
            ("database", DatabaseFrame(self.db, self.notifier), "🗄 База данных"),
            ("settings", SettingsFrame(self.notifier, self._on_theme_applied), "🎨 Темы"),
        ]
        for key, frame, label in tabs_def:
            self._frames[key] = frame
            self.tabs.addTab(frame, label)

        self._layout.addWidget(self.tabs, stretch=1)

    # --- Status bar ---

    def _create_status_bar(self) -> None:
        sb = QStatusBar()
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)

        self._status = QLabel("  Готов")
        sb.addWidget(self._status, 1)

        sc = QLabel(
            "Ctrl+1…7: вкладки  │  Ctrl+R / F5: обновить  │  "
            "Ctrl+E: ред.  │  Ctrl+D: удал.  │  Ctrl+F: поиск"
        )
        sb.addWidget(sc, 2)
        sb.addPermanentWidget(QLabel(f"  📁 {os.path.basename(str(self.db.db_path))}  "))

    def set_status(self, text: str) -> None:
        self._status.setText(text)

    # --- Shortcuts ---

    def _bind_shortcuts(self) -> None:
        for i in range(7):
            QShortcut(QKeySequence(f"Ctrl+{i+1}"), self).activated.connect(
                lambda idx=i: self.tabs.setCurrentIndex(idx)
            )
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self.refresh_data)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.refresh_data)
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(self._edit)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self._delete)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self._search)
        QShortcut(QKeySequence("F12"), self).activated.connect(self._debugger)

    def _edit(self) -> None:
        f = self._frames.get("clients")
        if f and hasattr(f, "edit_selected"):
            f.edit_selected()

    def _delete(self) -> None:
        f = self._frames.get("clients")
        if f and hasattr(f, "delete_selected"):
            f.delete_selected()

    def _search(self) -> None:
        f = self._frames.get("clients")
        if f and hasattr(f, "focus_search"):
            f.focus_search()

    def _debugger(self) -> None:
        try:
            from debugger import toggle_debugger
            toggle_debugger()
        except ImportError:
            logger.warning("Модуль отладчика недоступен (требуется customtkinter)")
            self.notifier.show_info("Отладчик недоступен в этой сборке")
        except Exception as e:
            logger.error("Ошибка отладчика: %s", e)

    # --- Data / Theme ---

    def refresh_data(self) -> None:
        try:
            for frame in self._frames.values():
                if hasattr(frame, "refresh"):
                    frame.refresh()
            # Авто-экспорт в Excel после любого изменения
            from gui_qt.exporters import auto_export_all
            auto_export_all(self.db)
            self.set_status("Данные обновлены")
        except Exception as e:
            self.set_status(f"Ошибка: {str(e)[:40]}")
            self.notifier.show_error(f"Ошибка: {e}")

    def _on_theme_applied(self) -> None:
        self._apply_current_theme()
        self.theme_changed.emit()

    def _apply_current_theme(self) -> None:
        self.setStyleSheet(theme_engine.generate_qss())

    # --- Lifecycle ---

    def _center(self) -> None:
        r = self.screen().availableGeometry()
        self.move((r.width() - self.width()) // 2, (r.height() - self.height()) // 2)

    def closeEvent(self, event: QCloseEvent) -> None:
        if ConfirmDialog.confirm(self, "Выход", "Вы действительно хотите выйти?"):
            self.db.close()
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.notifier.isVisible():
            self.notifier._reposition()
