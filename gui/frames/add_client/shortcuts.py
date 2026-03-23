# -*- coding: utf-8 -*-

"""Горячие клавиши для формы добавления клиента"""
import tkinter as tk
import logging
from utils.clipboard import get_clipboard

logger = logging.getLogger(__name__)


class ShortcutManager:
    """Класс для управления горячими клавишами"""
    
    def __init__(self, parent, notifier=None):
        self.parent = parent
        self.notifier = notifier
        self.debug_mode = True
        self.clipboard = get_clipboard()
        print("✅ ShortcutManager для AddClient инициализирован")
    
    def bind_paste_to_entries(self, entries):
        """
        Привязывает Ctrl+V ко всем переданным полям ввода
        
        Args:
            entries: список полей ввода
        """
        print(f"\n🔧 Привязка Ctrl+V к {len(entries)} полям")
        for i, entry in enumerate(entries):
            self._bind_paste_to_entry(entry, f"поле_{i+1}")
    
    def _bind_paste_to_entry(self, entry, field_name):
        """Привязывает Ctrl+V к конкретному полю ввода"""
        
        def on_paste(event):
            """Обработчик вставки текста"""
            print(f"\n🔍 ===== ВСТАВКА В {field_name} =====")
            print(f"📌 Тип события: {event.type}")
            print(f"📌 Виджет: {event.widget}")
            print(f"📌 Класс виджета: {event.widget.__class__.__name__}")
            
            try:
                # Получаем текст из буфера обмена
                clipboard_text = self.clipboard.get_clipboard_text()
                
                if clipboard_text:
                    print(f"📋 Получен текст: {len(clipboard_text)} символов")
                    print(f"📋 Первые 50 символов: '{clipboard_text[:50]}'")
                    
                    # Очищаем текст
                    clean_text = ' '.join(clipboard_text.split())
                    
                    # Получаем текущее содержимое
                    current = entry.get()
                    cursor_pos = entry.index("insert")
                    print(f"📍 Текущий текст: '{current}'")
                    print(f"📍 Позиция курсора: {cursor_pos}")
                    
                    # Вставляем текст
                    if cursor_pos == "end" or not isinstance(cursor_pos, int):
                        new_text = current + clean_text
                        print("📌 Вставка в конец")
                    else:
                        new_text = current[:cursor_pos] + clean_text + current[cursor_pos:]
                        print(f"📌 Вставка в позицию {cursor_pos}")
                    
                    entry.delete(0, "end")
                    entry.insert(0, new_text)
                    
                    print(f"✅ Новый текст: '{new_text}'")
                    print(f"✅ Длина: {len(new_text)} символов")
                    
                    if self.notifier:
                        self.notifier.show_success(f"📋 Вставлено {len(clean_text)} символов")
                else:
                    print("⚠️ Буфер обмена пуст")
                    
            except Exception as e:
                print(f"❌ Ошибка вставки: {e}")
                import traceback
                traceback.print_exc()
                if self.notifier:
                    self.notifier.show_error("❌ Ошибка вставки")
            
            print(f"🔍 ===== КОНЕЦ =====\n")
            return "break"
        
        # Привязываем обработчик ВСЕМИ возможными способами
        entry.bind('<Control-v>', on_paste)
        entry.bind('<Control-V>', on_paste)
        entry.bind('<Command-v>', on_paste)
        entry.bind('<Command-V>', on_paste)
        entry.bind('<Shift-Insert>', on_paste)
        
        # Привязываем также на уровне класса
        entry.bind_class('Entry', '<Control-v>', on_paste)
        entry.bind_class('Entry', '<Control-V>', on_paste)
        
        print(f"✅ Привязан Ctrl+V к {field_name}")
    
    def bind_save_shortcut(self, entries, save_callback):
        """Привязывает Ctrl+Enter ко всем полям для сохранения"""
        def on_save(event):
            print("\n💾 ===== СОХРАНЕНИЕ =====")
            print(f"📌 Событие: {event}")
            print(f"📌 Виджет: {event.widget}")
            save_callback()
            print("💾 ===== КОНЕЦ =====\n")
            return "break"
        
        print("\n🔧 Привязка Ctrl+Enter")
        for i, entry in enumerate(entries):
            entry.bind('<Control-Return>', on_save)
            entry.bind('<Command-Return>', on_save)
            print(f"✅ Привязан Ctrl+Enter к полю {i+1}")
        
        print("✅ Привязан Ctrl+Enter для сохранения")
    
    def bind_clear_shortcut(self, entries, clear_callback):
        """Привязывает Ctrl+Q ко всем полям для очистки формы"""
        def on_clear(event):
            print("\n🔄 ===== ОЧИСТКА =====")
            print(f"📌 Событие: {event}")
            print(f"📌 Виджет: {event.widget}")
            clear_callback()
            print("🔄 ===== КОНЕЦ =====\n")
            return "break"
        
        print("\n🔧 Привязка Ctrl+Q")
        for i, entry in enumerate(entries):
            entry.bind('<Control-q>', on_clear)
            entry.bind('<Control-Q>', on_clear)
            entry.bind('<Command-q>', on_clear)
            entry.bind('<Command-Q>', on_clear)
            print(f"✅ Привязан Ctrl+Q к полю {i+1}")
        
        print("✅ Привязан Ctrl+Q для очистки")
    
    def test_shortcuts(self, entries):
        """Тестирование привязки клавиш"""
        print("\n🔧 ТЕСТИРОВАНИЕ ГОРЯЧИХ КЛАВИШ")
        for i, entry in enumerate(entries):
            print(f"Поле {i+1}: {entry}")
            # Проверяем, есть ли привязки
            bindings = entry.bind()
            print(f"   Привязки: {bindings}")