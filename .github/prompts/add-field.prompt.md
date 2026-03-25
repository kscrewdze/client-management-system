---
description: "Добавить новое поле в модель данных Client с миграцией БД и обновлением GUI"
agent: "architect"
---

Добавь новое поле в модель данных. Выполни ВСЕ шаги:

1. **Модель** (`database/models.py`):
   - Добавь поле в `@dataclass Client` с type hint
   - Обнови `from_db_row()` и `to_dict()`

2. **Миграция** (`database/core.py`):
   - Добавь `ALTER TABLE ... ADD COLUMN` в `_create_tables()` с обработкой `OperationalError`

3. **CRUD** (`database/clients.py`):
   - Обнови INSERT и UPDATE запросы

4. **GUI формы**:
   - Добавь поле в форму добавления (`gui/frames/add_client/form_widget.py`)
   - Добавь поле в форму редактирования (`gui/dialogs/edit_client/form_widget.py`)
   - Обнови таблицу клиентов если нужно

5. Проверь, что всё работает
