---
description: "Use when working with error handling, logging, exception patterns, or debugging. Enforces logging-over-print, specific exceptions, and graceful degradation."
---

# Правила обработки ошибок

## logging вместо print (СТРОГО)
```python
import logging
logger = logging.getLogger(__name__)

# ✅ ПРАВИЛЬНО
logger.info("Клиент добавлен: %s", name)
logger.error("Ошибка БД: %s", e)

# ❌ ЗАПРЕЩЕНО
print(f"✅ Клиент добавлен: {name}")
print(f"❌ Ошибка: {e}")
```

## Конкретные исключения
```python
# ✅ ПРАВИЛЬНО
except (OSError, json.JSONDecodeError) as e:
    logger.error("Ошибка чтения конфига: %s", e)
except sqlite3.OperationalError as e:
    logger.error("Ошибка SQL: %s", e)

# ❌ ЗАПРЕЩЕНО
except:
    pass
except Exception:
    pass  # без логирования
```

## Tkinter ошибки
```python
# Уничтожение виджетов — ожидаемая ошибка при закрытии
try:
    widget.destroy()
except Exception as e:
    logger.debug("Виджет уже уничтожен: %s", e)
```
