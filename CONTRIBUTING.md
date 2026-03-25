# Contributing / Участие в проекте

Спасибо за интерес к проекту! Вот как вы можете помочь.

## 🐛 Нашли баг?

1. Проверьте [Issues](https://github.com/kscrewdze/client-management-system/issues) — возможно, баг уже известен
2. Если нет — создайте новый Issue с описанием:
   - Что ожидалось
   - Что произошло
   - Шаги воспроизведения
   - Версия Python и ОС

## 💡 Хотите предложить улучшение?

Создайте Issue с тегом `enhancement` и опишите вашу идею.

## 🔧 Хотите внести изменения?

### Подготовка

```bash
# Форк и клонирование
git clone https://github.com/<ваш-username>/client-management-system.git
cd client-management-system

# Виртуальное окружение
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS

# Зависимости
pip install -r requirements.txt
```

### Процесс

1. Создайте ветку от `master`:
   ```bash
   git checkout -b feature/моя-фича
   ```
2. Внесите изменения
3. Убедитесь, что тесты проходят:
   ```bash
   pytest
   ```
4. Сделайте коммит с понятным сообщением:
   ```bash
   git commit -m "feat: добавлена новая функция X"
   ```
5. Отправьте Pull Request

### Стиль кода

- Классы: `PascalCase`, функции: `snake_case`, константы: `UPPER_SNAKE_CASE`
- Приватные методы: `_leading_underscore`
- Файлы начинаются с `# -*- coding: utf-8 -*-`
- Комментарии и UI-текст на **русском языке**
- Type hints обязательны
- Импорты: stdlib → third-party → local

### Префиксы коммитов

| Префикс | Назначение |
|---------|------------|
| `feat:` | Новая функциональность |
| `fix:` | Исправление бага |
| `docs:` | Документация |
| `style:` | Форматирование (без логических изменений) |
| `refactor:` | Рефакторинг |
| `test:` | Тесты |
| `chore:` | Обслуживание (зависимости, конфиги) |
