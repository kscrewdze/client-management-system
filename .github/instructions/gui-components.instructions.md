---
description: "Use when editing GUI frames, dialogs, or widgets. Enforces CustomTkinter patterns: create_widgets, theme colors, callback pattern, layout rules."
applyTo: gui/**/*.py, widgets/**/*.py
---

# Правила GUI-компонентов

## Структура Frame
```python
class MyFrame(ctk.CTkFrame):
    def __init__(self, parent, db, **kwargs):
        super().__init__(parent, **kwargs)
        self.db = db
        self.create_widgets()

    def create_widgets(self) -> None:
        """Создание и размещение виджетов."""
        ...
```

## Цвета
НЕ хардкодь — бери из темы:
```python
# Правильно
color = self.theme.get("primary_color")
# Неправильно
color = "#2B5B84"
```

## Layout
- `grid()` для сложных сеток, `pack()` для линейных
- `grid_columnconfigure(0, weight=1)` для адаптивности
- `padx`, `pady` для отступов

## Callbacks
Frames получают колбэки в `__init__`. Диалоги возвращают результат через callback.
