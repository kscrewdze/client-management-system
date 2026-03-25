# Client Manager — Workspace Instructions

## Project Overview
Desktop CRM-приложение для управления клиентами. GUI на CustomTkinter, база данных SQLite3, упаковка через PyInstaller.

## Tech Stack
- **Python 3.10+**, **CustomTkinter 5.2.2**, **SQLite3**
- **Pillow** (изображения), **openpyxl/pandas** (экспорт), **python-dateutil** (даты)
- Все зависимости в `requirements.txt`

## Architecture
- **Layered**: GUI → Frames/Dialogs → Database/Business Logic → Utils
- **Database** делегирует через sub-модули: `ClientsDB`, `MatricesDB`, `SearchDB`, `StatisticsDB`
- **Themes** управляются через `ThemeManager` с наследованием от `BaseTheme`
- **Frames** — самодостаточные `ctk.CTkFrame` с `create_widgets()` паттерном

## Code Style
- Классы: `PascalCase`, функции/методы: `snake_case`, константы: `UPPER_SNAKE_CASE`
- Приватные методы/атрибуты: `_leading_underscore`
- Все `.py` файлы начинаются с `# -*- coding: utf-8 -*-`
- Комментарии и UI-текст на **русском языке**
- Docstrings: module-level с author/version, методы с Args/Returns/Raises
- Type hints обязательны для параметров и возвращаемых значений
- Импорты: stdlib → third-party → local, разделённые пустой строкой

## Patterns
- **Callback/Observer**: главное окно передаёт колбэки (`refresh_data`) фреймам
- **Delegation**: `Database` → `ClientsDB`, `MatricesDB`, etc.
- **Dataclass Models**: `@dataclass` + `from_db_row()` + `to_dict()`
- **Manager pattern**: `ThemeManager`, `TabsManager`, `ShortcutManager`

## Database Conventions
- Потокобезопасность: все операции через `_lock`
- Параметризованные SQL-запросы (защита от инъекций)
- Миграции схемы при инициализации в `_create_tables()`
- `sqlite3.Row` для доступа по имени колонки

## GUI Conventions
- Каждый frame наследуется от `ctk.CTkFrame`
- UI строится в `create_widgets()`, не в `__init__`
- Цвета берутся из текущей темы, не хардкодятся
- Ошибки tkinter обрабатываются через `tk_error_handler`
- Клавиатурные шорткаты регистрируются через `Shortcuts` модуль

## Error Handling
- `try/except` с logging для всех операций с БД и файлами
- Graceful degradation — приложение не должно падать
- Потоки: используй блокировки (`threading.Lock`)

## Build & Run
- Запуск: `python main.py`
- Установка зависимостей: `pip install -r requirements.txt`
- Сборка exe: PyInstaller с `build_exe_hooks.py`
- Проверка frozen-режима: `getattr(sys, 'frozen', False)`
