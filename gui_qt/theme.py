# -*- coding: utf-8 -*-

"""
Движок тем — генерация QSS из ThemeColors.
Компактный QSS-генератор с полным набором стилей.
"""
import json
import logging
import os
from datetime import datetime
from typing import Dict, Optional

from themes.themes.base_theme import BaseTheme, ThemeColors
from themes.themes.emerald import emerald
from themes.themes.sapphire import sapphire
from themes.themes.ruby import ruby
from themes.themes.amethyst import amethyst
from themes.themes.midnight import midnight
from themes.themes.sunrise import sunrise

logger = logging.getLogger(__name__)

# Сокращение для повторяющегося CSS
_FONT = '"Segoe UI"'
_RADIUS = "6px"
_RADIUS_SM = "4px"


class ThemeEngine:
    """Движок тем — генерирует QSS из ThemeColors."""

    def __init__(self) -> None:
        self.themes: Dict[str, BaseTheme] = {
            "emerald": emerald, "sapphire": sapphire, "ruby": ruby,
            "amethyst": amethyst, "midnight": midnight, "sunrise": sunrise,
        }
        self.current_theme: Optional[BaseTheme] = None
        # Конфиг темы пишется рядом с .exe (APP_DIR), чтобы настройки сохранялись
        from config.settings import Settings
        self._config_file = os.path.join(str(Settings.APP_DIR), "theme_config.json")
        # Fallback: читаем из исходной папки для dev-режима
        self._config_file_bundled = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "themes", "theme_config.json",
        )
        self._load_config()
        logger.info("ThemeEngine: загружено %d тем", len(self.themes))

    # --- Публичные ---

    def get_all_themes(self) -> Dict[str, str]:
        return {k: t.description for k, t in self.themes.items()}

    def get_theme(self, name: str) -> Optional[BaseTheme]:
        return self.themes.get(name)

    def get_current_theme(self) -> Optional[BaseTheme]:
        return self.current_theme

    def colors(self) -> ThemeColors:
        return (self.current_theme or self.themes["emerald"]).colors

    def apply_theme(self, name: str) -> bool:
        if name not in self.themes:
            return False
        self.current_theme = self.themes[name]
        self._save_config(name)
        logger.info("ThemeEngine: применена тема '%s'", self.current_theme.name)
        return True

    def is_dark(self) -> bool:
        return bool(self.current_theme and "Полуночная" in self.current_theme.name)

    # --- QSS-генератор ---

    def generate_qss(self) -> str:
        c = self.colors()
        r, rs = _RADIUS, _RADIUS_SM
        f = _FONT

        # Вспомогательная: кнопка-вариант
        def btn(cls: str, bg: str, hover: str, pressed: str) -> str:
            return (
                f'QPushButton[cssClass="{cls}"]{{background:{bg};}}'
                f'QPushButton[cssClass="{cls}"]:hover{{background:{hover};}}'
                f'QPushButton[cssClass="{cls}"]:pressed{{background:{pressed};}}'
            )

        return f"""
/* === Глобальные === */
*{{font-family:{f};}}
QMainWindow{{background:{c.background};}}
QDialog{{background:{c.background};}}

/* === Типографика === */
QLabel{{color:{c.text_primary};font-size:11px;}}
QLabel[cssClass="title"]{{font-size:14px;font-weight:700;color:{c.primary};letter-spacing:1px;}}
QLabel[cssClass="subtitle"]{{font-size:12px;font-weight:700;color:{c.primary};}}
QLabel[cssClass="hint"]{{font-size:10px;color:{c.text_secondary};}}
QLabel[cssClass="destiny"]{{font-weight:700;color:{c.accent};font-size:11px;}}

/* === Карточки === */
QFrame[cssClass="card"]{{background:{c.background_secondary};border:1px solid {c.border};border-radius:10px;}}
QFrame[cssClass="card-elevated"]{{background:{c.background_secondary};border:1px solid {c.border};border-radius:10px;}}
QFrame[cssClass="transparent"]{{background:transparent;border:none;}}
QFrame[cssClass="separator"]{{background:{c.border};max-height:1px;min-height:1px;border:none;}}

/* === Вкладки === */
QTabWidget::pane{{border:1px solid {c.border};border-radius:{rs};background:{c.background};top:-1px;}}
QTabBar{{qproperty-drawBase:0;}}
QTabBar::tab{{background:{c.background_secondary};color:{c.text_secondary};padding:6px 16px;margin-right:2px;border-top-left-radius:{r};border-top-right-radius:{r};font-size:11px;font-weight:600;border-bottom:3px solid transparent;}}
QTabBar::tab:selected{{background:{c.background};color:{c.primary};border-bottom:3px solid {c.primary};}}
QTabBar::tab:hover:!selected{{background:{c.background_hover};color:{c.text_primary};border-bottom:3px solid {c.border};}}

/* === Кнопки === */
QPushButton{{background:{c.primary};color:{c.text_inverse};border:none;border-radius:{r};padding:5px 14px;font-size:11px;font-weight:600;min-height:20px;}}
QPushButton:hover{{background:{c.secondary};}}
QPushButton:pressed{{background:{c.highlight};padding:6px 14px 4px 14px;}}
QPushButton:disabled{{background:{c.text_disabled};color:{c.background_hover};}}
{btn("success", c.success, "#1e8a27", "#166d1d")}
{btn("warning", c.warning, "#db6a00", "#c45f00")}
{btn("danger", c.error, "#b71c1c", "#8e1515")}
{btn("info", c.info, "#0277bd", "#015f96")}
QPushButton[cssClass="flat"]{{background:transparent;color:{c.text_primary};border:1px solid {c.border};}}
QPushButton[cssClass="flat"]:hover{{background:{c.background_hover};border-color:{c.text_secondary};}}
QPushButton[cssClass="outline-primary"]{{background:transparent;color:{c.primary};border:2px solid {c.primary};}}
QPushButton[cssClass="outline-primary"]:hover{{background:{c.primary};color:{c.text_inverse};}}

/* === Поля ввода === */
QLineEdit,QTextEdit{{background:{c.background_widget};color:{c.text_primary};border:1px solid {c.border};border-radius:{r};padding:4px 10px;font-size:11px;selection-background-color:{c.highlight};}}
QLineEdit:focus,QTextEdit:focus{{border:2px solid {c.border_focus};padding:3px 9px;}}
QLineEdit:disabled{{background:{c.background_hover};color:{c.text_disabled};}}
QLineEdit:hover,QTextEdit:hover{{border:1px solid {c.text_secondary};}}
QLineEdit:focus:hover,QTextEdit:focus:hover{{border:2px solid {c.border_focus};}}

/* === ComboBox === */
QComboBox{{background:{c.background_widget};color:{c.text_primary};border:1px solid {c.border};border-radius:{r};padding:4px 10px;font-size:11px;min-height:18px;}}
QComboBox:hover{{border:1px solid {c.text_secondary};}}
QComboBox:focus{{border:2px solid {c.border_focus};}}
QComboBox::drop-down{{border:none;width:26px;subcontrol-origin:padding;subcontrol-position:top right;}}
QComboBox::down-arrow{{width:10px;height:10px;}}
QComboBox QAbstractItemView{{background:{c.background_widget};color:{c.text_primary};selection-background-color:{c.highlight};selection-color:{c.text_inverse};border:1px solid {c.border};border-radius:{rs};padding:2px;outline:none;}}
QComboBox QAbstractItemView::item{{padding:4px 8px;min-height:22px;}}
QComboBox QAbstractItemView::item:hover{{background:{c.background_hover};}}

/* === Таблица === */
QTableView,QTreeView{{background:{c.background_widget};alternate-background-color:{c.background_secondary};color:{c.text_primary};border:1px solid {c.border};border-radius:{rs};gridline-color:{c.border};font-size:11px;selection-background-color:{c.highlight};selection-color:{c.text_inverse};outline:none;}}
QTableView::item{{padding:3px 6px;border-bottom:1px solid {c.border};}}
QTableView::item:selected{{background:{c.highlight};color:{c.text_inverse};}}
QTableView::item:selected:hover{{background:{c.secondary};color:{c.text_inverse};}}
QTableView::item:hover{{background:{c.background_hover};}}
QHeaderView::section{{background:{c.primary};color:{c.text_inverse};padding:5px 8px;border:none;border-right:1px solid {c.secondary};font-size:10px;font-weight:600;}}
QHeaderView::section:hover{{background:{c.secondary};}}

/* === Скролл === */
QScrollBar:vertical{{background:transparent;width:10px;border-radius:5px;margin:2px;}}
QScrollBar::handle:vertical{{background:{c.border};border-radius:4px;min-height:30px;margin:1px;}}
QScrollBar::handle:vertical:hover{{background:{c.text_secondary};}}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{{background:transparent;}}
QScrollBar:horizontal{{background:transparent;height:10px;border-radius:5px;margin:2px;}}
QScrollBar::handle:horizontal{{background:{c.border};border-radius:4px;min-width:30px;margin:1px;}}
QScrollBar::handle:horizontal:hover{{background:{c.text_secondary};}}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{{width:0;}}
QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{{background:transparent;}}

/* === Splitter === */
QSplitter::handle{{background:{c.border};}}
QSplitter::handle:vertical{{height:3px;margin:1px 30px;border-radius:1px;}}
QSplitter::handle:horizontal{{width:3px;margin:30px 1px;border-radius:1px;}}
QSplitter::handle:hover{{background:{c.text_secondary};}}

/* === Checkbox / Radio === */
QCheckBox{{color:{c.text_primary};font-size:11px;spacing:6px;}}
QCheckBox::indicator{{width:16px;height:16px;border:2px solid {c.border};border-radius:4px;background:{c.background_widget};}}
QCheckBox::indicator:hover{{border-color:{c.primary};}}
QCheckBox::indicator:checked{{background:{c.primary};border-color:{c.primary};}}

/* === StatusBar === */
QStatusBar{{background:{c.background_secondary};color:{c.text_secondary};font-size:9px;border-top:1px solid {c.border};padding:2px 0;}}
QStatusBar QLabel{{font-size:9px;color:{c.text_secondary};}}

/* === Tooltip === */
QToolTip{{background:{c.background_widget};color:{c.text_primary};border:1px solid {c.border};border-radius:{rs};padding:6px 10px;font-size:10px;}}

/* === ProgressBar === */
QProgressBar{{background:{c.background_secondary};border:1px solid {c.border};border-radius:{r};text-align:center;font-size:10px;color:{c.text_primary};min-height:8px;}}
QProgressBar::chunk{{background:{c.primary};border-radius:5px;}}

/* === Menu === */
QMenuBar{{background:{c.background_secondary};color:{c.text_primary};}}
QMenuBar::item:selected{{background:{c.highlight};color:{c.text_inverse};border-radius:{rs};}}

/* === GroupBox === */
QGroupBox{{border:1px solid {c.border};border-radius:{r};margin-top:8px;padding-top:12px;font-weight:600;color:{c.text_primary};}}
QGroupBox::title{{subcontrol-origin:margin;subcontrol-position:top left;padding:0 6px;color:{c.primary};}}
"""

    # --- Конфиг ---

    def _load_config(self) -> None:
        # Пробуем APP_DIR (пользовательские настройки), затем bundled (по умолчанию)
        for cfg_path in (self._config_file, self._config_file_bundled):
            try:
                if os.path.exists(cfg_path):
                    with open(cfg_path, "r", encoding="utf-8") as fh:
                        name = json.load(fh).get("theme")
                        if name and name in self.themes:
                            self.current_theme = self.themes[name]
                            logger.info("ThemeEngine: загружена тема '%s' из %s", name, cfg_path)
                            return
            except (OSError, json.JSONDecodeError) as e:
                logger.error("ThemeEngine: ошибка конфига %s: %s", cfg_path, e)
        self.current_theme = self.themes["emerald"]

    def _save_config(self, theme_name: str) -> None:
        try:
            with open(self._config_file, "w", encoding="utf-8") as fh:
                json.dump(
                    {"theme": theme_name, "saved_at": datetime.now().isoformat()},
                    fh, indent=2, ensure_ascii=False,
                )
        except OSError as e:
            logger.error("ThemeEngine: ошибка сохранения: %s", e)


theme_engine = ThemeEngine()
