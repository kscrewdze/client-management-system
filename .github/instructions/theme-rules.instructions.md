---
description: "Use when creating or modifying themes, color schemes, appearance modes, or BaseTheme subclasses. Enforces theme architecture: color dataclass, BaseTheme inheritance, ThemeManager registration."
applyTo: themes/**/*.py
---

# Правила тем оформления

## Структура темы
```python
# themes/themes/<name>.py
from themes.themes.base_theme import BaseTheme, ThemeColors

colors = ThemeColors(
    background="#...",
    primary="#...",
    secondary="#...",
    ...
)

<name> = BaseTheme(
    name="Название темы",
    description="Описание",
    colors=colors
)
```

## Регистрация
Новая тема ОБЯЗАНА быть зарегистрирована в `themes/manager.py`:
```python
from themes.themes.<name> import <name>
# + добавить в self.themes
```

## Правила
- Все цвета — через `ThemeColors` dataclass
- Тёмная тема — имя содержит "Полуночная" (для auto dark mode)
- Цвета должны быть контрастными и читаемыми
