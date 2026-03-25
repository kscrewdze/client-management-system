---
description: "Use when editing database modules, SQL queries, models, or migration code. Enforces thread safety, parameterized queries, and delegation pattern."
applyTo: "database/**/*.py"
---

# Правила Database-модулей

## Безопасность SQL
ВСЕГДА параметризованные запросы:
```python
# Правильно
cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
# ЗАПРЕЩЕНО
cursor.execute(f"SELECT * FROM clients WHERE id = {client_id}")
```

## Потокобезопасность
Все операции с БД через блокировку:
```python
def get_client(self, client_id: int) -> Optional[Client]:
    with self._lock:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        return Client.from_db_row(row) if row else None
```

## Модели
- `@dataclass` с `from_db_row()` и `to_dict()`
- `sqlite3.Row` для доступа по имени колонки

## Делегирование
Новая функциональность — в соответствующий sub-модуль:
- Клиенты → `clients.py`
- Матрицы → `matrices.py`
- Поиск → `search.py`
- Статистика → `statistics.py`
