---
description: "Use when editing any Python file. Enforces project coding standards: UTF-8 header, type hints, Russian comments, import order, error handling."
applyTo: "**/*.py"
---

# Стандарты Python-кода

## Заголовок файла
Каждый `.py` файл ОБЯЗАН начинаться с:
```python
# -*- coding: utf-8 -*-
```

## Type Hints
Обязательны для всех параметров и возвращаемых значений:
```python
def get_client(self, client_id: int) -> Optional[Client]:
```

## Язык
- Комментарии — на русском
- UI-текст — на русском
- Имена переменных/функций — на английском

## Обработка ошибок
- `try/except` с конкретными исключениями, НЕ голый `except:`
- Логирование через `logging`, НЕ `print()`
- Приложение не должно падать — graceful degradation
