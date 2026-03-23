# -*- coding: utf-8 -*-

"""Тест отладчика"""
import sys
import os

print("=" * 50)
print("🔍 ТЕСТ ОТЛАДЧИКА")
print("=" * 50)

# Проверяем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Текущая директория: {current_dir}")

# Проверяем наличие папки debugger
debugger_path = os.path.join(current_dir, "debugger")
if os.path.exists(debugger_path):
    print(f"✅ Папка debugger найдена: {debugger_path}")
    print(f"   Содержимое: {os.listdir(debugger_path)}")
else:
    print(f"❌ Папка debugger НЕ найдена по пути: {debugger_path}")

# Проверяем путь в sys.path
print(f"\n📌 sys.path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

# Пробуем импортировать
print(f"\n🔧 Пробуем импортировать отладчик...")
try:
    from debugger import toggle_debugger
    print("✅ Импорт успешен!")
    print(f"   Функция: {toggle_debugger}")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    
    # Пробуем альтернативный импорт
    try:
        import debugger
        print(f"✅ debugger импортирован как модуль")
        print(f"   Атрибуты: {dir(debugger)}")
    except ImportError as e2:
        print(f"❌ Не удалось импортировать даже модуль: {e2}")

print("\n" + "=" * 50)