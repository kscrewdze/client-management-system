# -*- coding: utf-8 -*-

"""
Общие утилиты GUI — убирает дублирование между фреймами и диалогами.
"""
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QWidget,
)

from database.utils import calculate_destiny_number
from utils.date_parser import DateParser

logger = logging.getLogger(__name__)

_H = 28  # Высота полей ввода

# Определение полей клиента (label, key, placeholder)
CLIENT_FIELDS: List[Tuple[str, str, str]] = [
    ("Имя:*", "name", "Иванов Иван"),
    ("Telegram:", "telegram", "@username"),
    ("Телефон:", "phone", "+7 (999) 123-45-67"),
    ("Дата рождения:*", "birth_date", "дд.мм.гггг или 26011982"),
    ("Дата заказа:*", "order_date", "дд.мм.гггг или 26012024"),
    ("Комментарий:", "comment", "Необязательно"),
]


def build_client_form(
    grid: QGridLayout, start_row: int = 0,
) -> Tuple[Dict[str, QLineEdit], QComboBox, QLineEdit, QLabel, QLineEdit, int]:
    """Построить общую форму клиента.

    Returns:
        (entries, matrix_combo, price_entry, destiny_label, custom_name_entry, next_row)
    """
    entries: Dict[str, QLineEdit] = {}
    destiny_label: Optional[QLabel] = None
    row = start_row

    from datetime import datetime
    today = datetime.now().strftime("%d.%m.%Y")

    for label_text, key, placeholder in CLIENT_FIELDS:
        lbl = QLabel(label_text)
        lbl.setFixedWidth(120)
        grid.addWidget(lbl, row, 0, Qt.AlignRight | Qt.AlignVCenter)

        if key == "birth_date":
            # Дата рождения + число судьбы в одну строку
            bd_row = QHBoxLayout()
            bd_row.setSpacing(6)
            entry = QLineEdit()
            entry.setPlaceholderText(placeholder)
            entry.setFixedHeight(_H)
            bd_row.addWidget(entry, stretch=1)

            destiny_label = QLabel("ЧС: —")
            destiny_label.setFixedWidth(55)
            destiny_label.setProperty("cssClass", "destiny")
            bd_row.addWidget(destiny_label)
            grid.addLayout(bd_row, row, 1)
        else:
            entry = QLineEdit()
            entry.setPlaceholderText(placeholder)
            entry.setFixedHeight(_H)
            if key == "order_date":
                entry.setText(today)
            grid.addWidget(entry, row, 1)

        entries[key] = entry
        row += 1

    # Матрица + цена
    lbl_m = QLabel("Матрица:*")
    lbl_m.setFixedWidth(120)
    grid.addWidget(lbl_m, row, 0, Qt.AlignRight | Qt.AlignVCenter)

    m_row = QHBoxLayout()
    m_row.setSpacing(6)
    matrix_combo = QComboBox()
    matrix_combo.setMinimumWidth(180)
    matrix_combo.setFixedHeight(_H)
    m_row.addWidget(matrix_combo, stretch=1)

    m_row.addWidget(QLabel("Цена:"))
    price_entry = QLineEdit()
    price_entry.setPlaceholderText("0")
    price_entry.setFixedWidth(100)
    price_entry.setFixedHeight(_H)
    m_row.addWidget(price_entry)
    m_row.addWidget(QLabel("₽"))
    grid.addLayout(m_row, row, 1)
    row += 1

    # Поле для своего названия матрицы (скрыто по умолчанию)
    custom_name_entry = QLineEdit()
    custom_name_entry.setPlaceholderText("Название матрицы (свой выбор)")
    custom_name_entry.setFixedHeight(_H)
    custom_name_entry.setVisible(False)
    grid.addWidget(custom_name_entry, row, 1)

    return entries, matrix_combo, price_entry, destiny_label, custom_name_entry, row + 1


def update_destiny_display(text: str, label: QLabel) -> None:
    """Обновить отображение числа судьбы при вводе даты."""
    text = text.strip()
    if not text or len(text) < 6:
        label.setText("ЧС: —")
        return
    clean = re.sub(r'[.\-/]', '', text)
    if not clean.isdigit() or len(clean) < 6:
        label.setText("ЧС: —")
        return
    num = calculate_destiny_number(text)
    label.setText(f"ЧС: {num}" if num else "ЧС: —")


# ======================================================================
# Загрузка матриц
# ======================================================================

def load_matrices_combo(
    db: Any, combo: QComboBox, add_empty: bool = True,
) -> Dict[str, Tuple[str, Optional[int], float]]:
    """Загрузить матрицы из БД в QComboBox.

    Returns:
        mapping {display_text: (name, id, price)}
    """
    matrices = db.get_all_matrices()
    combo.blockSignals(True)
    combo.clear()
    mapping: Dict[str, Tuple[str, Optional[int], float]] = {}
    if add_empty:
        combo.addItem("")
    for m in matrices:
        display = f"{m.name} — {m.price:,.0f} ₽".replace(",", " ")
        mapping[display] = (m.name, m.id, m.price)
        combo.addItem(display)
    combo.addItem("✨ Свой выбор")
    combo.blockSignals(False)
    return mapping


def on_matrix_selected(
    text: str, mapping: Dict, price_entry: QLineEdit,
    custom_name_entry: Optional[QLineEdit] = None,
) -> None:
    """Обработчик выбора матрицы — проставляет цену, показывает/скрывает поле."""
    is_custom = "Свой выбор" in text
    if custom_name_entry:
        custom_name_entry.setVisible(is_custom)
    info = mapping.get(text)
    if info:
        price_entry.setText(str(int(info[2])))
    elif is_custom:
        price_entry.clear()
        if custom_name_entry:
            custom_name_entry.setFocus()
        else:
            price_entry.setFocus()


# ======================================================================
# Валидация / парсинг
# ======================================================================

def parse_price(text: str) -> Optional[float]:
    """Разобрать строку цены → float или None."""
    text = text.strip().replace(",", ".").replace(" ", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def validate_client_form(
    entries: Dict[str, QLineEdit],
    price_entry: QLineEdit,
    matrix_text: str,
    notifier: Any,
) -> Optional[Dict[str, Any]]:
    """Валидировать форму клиента.

    Returns:
        Словарь с parsed данными или None при ошибке.
    """
    name = entries["name"].text().strip()
    if not name:
        notifier.show_error("Введите имя клиента!")
        entries["name"].setFocus()
        return None

    birth_str = entries["birth_date"].text().strip()
    order_str = entries["order_date"].text().strip()
    if not birth_str:
        notifier.show_error("Введите дату рождения!")
        return None
    if not order_str:
        notifier.show_error("Введите дату заказа!")
        return None

    birth_date = DateParser.parse(birth_str)
    order_date = DateParser.parse(order_str)
    if not birth_date:
        notifier.show_error("Неверный формат даты рождения!")
        return None
    if not order_date:
        notifier.show_error("Неверный формат даты заказа!")
        return None

    if not matrix_text or matrix_text == "":
        notifier.show_error("Выберите матрицу!")
        return None
    if "Свой выбор" in matrix_text:
        # Для «свой выбор» матрица не обязательна — проверяется снаружи
        pass

    price = parse_price(price_entry.text())
    if price is None:
        notifier.show_error("Введите корректную цену!")
        return None

    return {
        "name": name,
        "telegram": entries["telegram"].text().strip() or None,
        "phone": entries["phone"].text().strip() or None,
        "birth_date": birth_date,
        "order_date": order_date,
        "comment": entries["comment"].text().strip() or None,
        "price": price,
    }


def fmt_price(value: float) -> str:
    """Формат цены: 1 234 ₽"""
    return f"{value:,.0f} ₽".replace(",", " ")
