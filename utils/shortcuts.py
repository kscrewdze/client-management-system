# -*- coding: utf-8 -*-

"""Модуль для управления горячими клавишами и вставкой текста"""
import tkinter as tk
import logging
from utils.clipboard import get_clipboard

logger = logging.getLogger(__name__)


class ShortcutManager:
    """Класс для управления горячими клавишами"""
    
    def __init__(self, notifier=None):
        self.notifier = notifier
        self.debug_mode = True
        self.clipboard = get_clipboard()
        print("✅ ShortcutManager инициализирован")
    
    def bind_paste_to_entries(self, entries):
        """
        Привязывает Ctrl+V ко всем переданным полям ввода
        
        Args:
            entries: список полей ввода
        """
        for i, entry in enumerate(entries):
            self._bind_paste_to_entry(entry, f"поле_{i+1}")
    
    def _bind_paste_to_entry(self, entry, field_name):
        """Привязывает Ctrl+V к конкретному полю ввода"""
        
        def on_paste(event):
            """Обработчик вставки текста"""
            print(f"\n🔍 ===== ВСТАВКА В {field_name} =====")
            
            try:
                # Получаем текст из буфера обмена через наш менеджер
                clipboard_text = self.clipboard.get_clipboard_text()
                
                if clipboard_text:
                    print(f"📋 Получен текст: {len(clipboard_text)} символов")
                    print(f"📋 Первые 50 символов: '{clipboard_text[:50]}...'")
                    
                    # Очищаем текст
                    clean_text = ' '.join(clipboard_text.split())
                    
                    # Получаем текущее содержимое
                    current = entry.get()
                    cursor_pos = entry.index("insert")
                    
                    # Вставляем текст
                    if cursor_pos == "end" or not isinstance(cursor_pos, int):
                        new_text = current + clean_text
                    else:
                        new_text = current[:cursor_pos] + clean_text + current[cursor_pos:]
                    
                    # Обновляем поле
                    entry.delete(0, "end")
                    entry.insert(0, new_text)
                    
                    print(f"✅ Текст вставлен. Новая длина: {len(new_text)}")
                    
                    if self.notifier:
                        self.notifier.show_success(f"📋 Вставлено {len(clean_text)} символов")
                else:
                    print("⚠️ Буфер обмена пуст")
                    
            except Exception as e:
                print(f"❌ Ошибка вставки: {e}")
                if self.notifier:
                    self.notifier.show_error("❌ Ошибка вставки")
            
            print(f"🔍 ===== КОНЕЦ =====\n")
            return "break"
        
        # Привязываем обработчик несколькими способами
        entry.bind('<Control-v>', on_paste)
        entry.bind('<Control-V>', on_paste)
        entry.bind('<Command-v>', on_paste)
        entry.bind('<Command-V>', on_paste)
        entry.bind('<Shift-Insert>', on_paste)
        
        # Также привязываем на уровне класса
        entry.bind_class('Entry', '<Control-v>', on_paste)
        entry.bind_class('Entry', '<Control-V>', on_paste)
        
        print(f"✅ Привязан Ctrl+V к {field_name}")
        return entry
    
    def bind_save_shortcut(self, entries, save_callback):
        """Привязывает Ctrl+Enter ко всем полям для сохранения"""
        def on_save(event):
            print("\n💾 ===== СОХРАНЕНИЕ =====")
            save_callback()
            print("💾 ===== КОНЕЦ =====\n")
            return "break"
        
        for entry in entries:
            entry.bind('<Control-Return>', on_save)
            entry.bind('<Command-Return>', on_save)
        
        print("✅ Привязан Ctrl+Enter для сохранения")
    
    def bind_clear_shortcut(self, entries, clear_callback):
        """Привязывает Ctrl+Q ко всем полям для очистки формы"""
        def on_clear(event):
            print("\n🔄 ===== ОЧИСТКА =====")
            clear_callback()
            print("🔄 ===== КОНЕЦ =====\n")
            return "break"
        
        for entry in entries:
            entry.bind('<Control-q>', on_clear)
            entry.bind('<Control-Q>', on_clear)
            entry.bind('<Command-q>', on_clear)
            entry.bind('<Command-Q>', on_clear)
        
        print("✅ Привязан Ctrl+Q для очистки")
    
    def test_clipboard(self):
        """Тестирование доступа к буферу обмена"""
        text = self.clipboard.get_clipboard_text()
        if text:
            print(f"📋 Буфер обмена содержит: '{text[:50]}...'")
            return True
        else:
            print("📋 Буфер обмена пуст")
            return False


# Создаем глобальный экземпляр
shortcut_manager = ShortcutManager()