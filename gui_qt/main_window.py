# -*- coding: utf-8 -*-

"""
Главное окно — QMainWindow с QTabWidget (7 вкладок).
Компактный header, status bar, keyboard shortcuts.
Ctrl+B: БД (диалог), F12: debug console.
"""
import logging
import os
from datetime import datetime
from typing import Dict, Optional

from PySide6.QtCore import Qt, QTimer, Signal, QPoint
from PySide6.QtGui import QShortcut, QKeySequence, QCloseEvent, QMouseEvent
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QStatusBar, QFrame, QPushButton,
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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(*Settings.APP_MIN_SIZE)
        self.resize(Settings.APP_WIDTH, Settings.APP_HEIGHT)

        self._drag_pos: Optional[QPoint] = None
        self._is_maximized = False

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
        self._first_refresh = True  # Skip auto-export on first load

        self._clock = QTimer(self)
        self._clock.timeout.connect(self._tick)
        self._clock.start(1000)
        self._center()
        logger.info("MainWindow инициализирован")

    # --- Header (custom title bar) ---

    def _create_header(self) -> None:
        tc = theme_engine.colors()

        title_bar = QFrame()
        title_bar.setFixedHeight(38)
        title_bar.setStyleSheet(
            f"QFrame{{background:{tc.primary};border:none;}}"
        )

        h = QHBoxLayout(title_bar)
        h.setContentsMargins(14, 0, 6, 0)
        h.setSpacing(0)

        # Left ornament
        ornament_l = QLabel("✦─◈─✦")
        ornament_l.setStyleSheet(
            "font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2px;"
            "background:transparent;border:none;"
        )
        h.addWidget(ornament_l)
        h.addStretch()

        # Centered title
        self._title = QLabel("◇  M A T R I X  ·  D E S T I N Y  ◇")
        self._title.setAlignment(Qt.AlignCenter)
        self._title.setStyleSheet(
            "font-size:12px;font-weight:700;color:rgba(255,255,255,0.95);"
            "letter-spacing:4px;background:transparent;border:none;"
        )
        h.addWidget(self._title)
        h.addStretch()

        # Right ornament
        ornament_r = QLabel("✦─◈─✦")
        ornament_r.setStyleSheet(
            "font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2px;"
            "background:transparent;border:none;"
        )
        h.addWidget(ornament_r)

        # Clock
        self._clock_lbl = QLabel()
        self._clock_lbl.setStyleSheet(
            "font-size:9px;color:rgba(255,255,255,0.5);background:transparent;"
            "border:none;padding-left:12px;"
        )
        h.addWidget(self._clock_lbl)
        self._tick()

        # Window control buttons
        _btn_css = (
            "QPushButton{{background:transparent;color:rgba(255,255,255,0.7);"
            "border:none;font-size:{sz}px;font-weight:bold;"
            "padding:0;min-width:36px;max-width:36px;min-height:38px;max-height:38px;}}"
            "QPushButton:hover{{background:rgba(255,255,255,0.15);}}"
        )
        _close_css = (
            "QPushButton{background:transparent;color:rgba(255,255,255,0.7);"
            "border:none;font-size:16px;font-weight:bold;"
            "padding:0;min-width:42px;max-width:42px;min-height:38px;max-height:38px;}"
            "QPushButton:hover{background:#e81123;color:#fff;}"
        )

        btn_min = QPushButton("─")
        btn_min.setStyleSheet(_btn_css.format(sz=12))
        btn_min.clicked.connect(self.showMinimized)
        h.addWidget(btn_min)

        self._btn_max = QPushButton("□")
        self._btn_max.setStyleSheet(_btn_css.format(sz=14))
        self._btn_max.clicked.connect(self._toggle_maximize)
        h.addWidget(self._btn_max)

        btn_close = QPushButton("✕")
        btn_close.setStyleSheet(_close_css)
        btn_close.clicked.connect(self.close)
        h.addWidget(btn_close)

        self._title_bar = title_bar
        self._layout.addWidget(title_bar)

        # Separator
        separator = QFrame()
        separator.setProperty("cssClass", "separator")
        self._layout.addWidget(separator)

    def _toggle_maximize(self) -> None:
        if self._is_maximized:
            self.showNormal()
            self._btn_max.setText("□")
            self._is_maximized = False
        else:
            self.showMaximized()
            self._btn_max.setText("❐")
            self._is_maximized = True

    # Title bar drag
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and event.position().y() < 38:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            if self._is_maximized:
                self._toggle_maximize()
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.position().y() < 38:
            self._toggle_maximize()
        else:
            super().mouseDoubleClickEvent(event)

    def _tick(self) -> None:
        self._clock_lbl.setText(datetime.now().strftime("%d.%m.%Y  %H:%M:%S"))

    # --- Tabs (lazy loading) ---

    def _create_tabs(self) -> None:
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self._frames: Dict[str, QWidget] = {}
        self._lazy_tabs: Dict[int, str] = {}  # index -> key (not yet created)

        # Only import & create the first two tabs eagerly (visible on startup)
        from gui_qt.frames.statistics_frame import StatisticsFrame
        from gui_qt.frames.clients_frame import ClientsFrame

        self._tab_defs = [
            ("statistics", "📊 Статистика"),
            ("clients", "👥 Клиенты"),
            ("matrices", "📐 Матрицы"),
            ("add", "➕ Добавить"),
            ("export", "📤 Экспорт"),
            ("settings", "🎨 Темы"),
            ("donate", "☕ Поддержка"),
        ]

        # Eagerly create first two tabs
        self._frames["statistics"] = StatisticsFrame(self.db, self.notifier)
        self._frames["clients"] = ClientsFrame(self.db, self.notifier, self.refresh_data)

        for idx, (key, label) in enumerate(self._tab_defs):
            if key in self._frames:
                self.tabs.addTab(self._frames[key], label)
            else:
                placeholder = QWidget()
                self.tabs.addTab(placeholder, label)
                self._lazy_tabs[idx] = key

        # Highlight "Поддержка" tab with accent color
        from PySide6.QtGui import QColor
        donate_idx = len(self._tab_defs) - 1  # last tab
        self.tabs.tabBar().setTabTextColor(donate_idx, QColor("#e8a317"))

        self.tabs.currentChanged.connect(self._on_tab_changed)
        self._layout.addWidget(self.tabs, stretch=1)

    def _on_tab_changed(self, index: int) -> None:
        """Lazily create tab content on first visit."""
        key = self._lazy_tabs.pop(index, None)
        if key is None:
            return
        frame = self._create_frame(key)
        if frame is None:
            return
        self._frames[key] = frame
        old = self.tabs.widget(index)
        self.tabs.removeTab(index)
        label = self._tab_defs[index][1]
        self.tabs.insertTab(index, frame, label)
        self.tabs.setCurrentIndex(index)
        old.deleteLater()
        if hasattr(frame, "refresh"):
            frame.refresh()

    def _create_frame(self, key: str) -> Optional[QWidget]:
        """Import and instantiate a frame by key (deferred)."""
        if key == "matrices":
            from gui_qt.frames.matrices_frame import MatricesFrame
            return MatricesFrame(self.db, self.notifier, self.refresh_data)
        if key == "add":
            from gui_qt.frames.add_client_frame import AddClientFrame
            return AddClientFrame(self.db, self.notifier, self.refresh_data)
        if key == "export":
            from gui_qt.frames.export_frame import ExportFrame
            return ExportFrame(self.db, self.notifier)
        if key == "settings":
            from gui_qt.frames.settings_frame import SettingsFrame
            return SettingsFrame(self.notifier, self._on_theme_applied)
        if key == "donate":
            from gui_qt.frames.donate_frame import DonateFrame
            return DonateFrame(self.notifier)
        return None

    # --- Status bar ---

    def _create_status_bar(self) -> None:
        sb = QStatusBar()
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)

        self._status = QLabel("  Готов")
        sb.addWidget(self._status, 1)

        sc = QLabel(
            "Ctrl+1…7: вкладки  │  Ctrl+R / F5: обновить  │  "
            "Ctrl+E: ред.  │  Ctrl+D: удал.  │  Ctrl+F: поиск  │  "
            "Ctrl+B: БД  │  F12 / Ctrl+`: консоль"
        )
        sb.addWidget(sc, 2)

        from version import VERSION
        sb.addPermanentWidget(QLabel(f"  v{VERSION}  │  📁 {os.path.basename(str(self.db.db_path))}  "))

    def set_status(self, text: str) -> None:
        self._status.setText(text)

    # --- Shortcuts ---

    def _bind_shortcuts(self) -> None:
        for i in range(min(len(self._tab_defs), 9)):
            QShortcut(QKeySequence(f"Ctrl+{i+1}"), self).activated.connect(
                lambda idx=i: self.tabs.setCurrentIndex(idx)
            )
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self.refresh_data)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.refresh_data)
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(self._edit)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self._delete)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self._search)
        QShortcut(QKeySequence("Ctrl+B"), self).activated.connect(self._open_database)
        QShortcut(QKeySequence("F12"), self).activated.connect(self._open_debug_console)
        QShortcut(QKeySequence("Ctrl+`"), self).activated.connect(self._open_debug_console)

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

    def _open_database(self) -> None:
        """Open Database Browser as a floating dialog (Ctrl+B)."""
        from gui_qt.dialogs.database_dialog import DatabaseDialog
        dlg = DatabaseDialog(self.db, self.notifier, parent=self)
        dlg.exec()

    def _open_debug_console(self) -> None:
        """Open developer debug console (F12)."""
        from gui_qt.dialogs.debug_console import DebugConsoleDialog
        dlg = DebugConsoleDialog(self.db, parent=self)
        dlg.exec()

    # --- Data / Theme ---

    def refresh_data(self) -> None:
        try:
            for frame in self._frames.values():
                if hasattr(frame, "refresh"):
                    frame.refresh()
            # Skip auto-export on first load to speed up startup
            if self._first_refresh:
                self._first_refresh = False
            else:
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
        # Update custom title bar color
        tc = theme_engine.colors()
        if hasattr(self, '_title_bar'):
            self._title_bar.setStyleSheet(
                f"QFrame{{background:{tc.primary};border:none;}}"
            )
        # Translucent window for glass theme
        current = theme_engine.get_current_theme()
        is_glass = current and current.name == "Стеклянная"
        self.setAttribute(Qt.WA_TranslucentBackground, is_glass)
        if is_glass:
            self.setWindowOpacity(0.92)
        else:
            self.setWindowOpacity(1.0)

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
