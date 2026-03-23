# -*- coding: utf-8 -*-

"""Менеджер вставки текста для диалогов"""
import tkinter as tk
import logging

logger = logging.getLogger(__name__)


class PasteManager:
    """Класс для управления вставкой текста в диалогах"""
    
    def __init__(self, dialog, notifier=None):
        """
        Инициализация менеджера вставки
        
        Args:
            dialog: диалоговое окно
            notifier: объект для уведомлений
        """
        self.dialog = dialog
        self.notifier = notifier
        print("✅ PasteManager инициализирован")
    
    def bind_paste_to_entry(self, entry, field_name):
        """Привязывает Ctrl+V к полю ввода"""
        
        def on_paste(event):
            """Обработчик вставки текста"""
            print(f"\n🔍 ===== ВСТАВКА В {field_name} =====")
            
            try:
                # Получаем текст из буфера обмена
                clipboard_text = self.dialog.clipboard_get()
                print(f"📋 Получен текст: '{clipboard_text[:50]}...'")
                
                if clipboard_text:
                    # Очищаем текст
                    clean_text = ' '.join(clipboard_text.split())
                    print(f"🧹 Очищенный текст: '{clean_text[:50]}...'")
                    
                    # Получаем текущую позицию курсора
                    try:
                        cursor_pos = entry.index("insert")
                        print(f"📍 Позиция курсора: {cursor_pos}")
                    except:
                        cursor_pos = "end"
                    
                    # Вставляем текст
                    if cursor_pos == "end" or not isinstance(cursor_pos, int):
                        # Вставляем в конец
                        current = entry.get()
                        new_text = current + clean_text
                        entry.delete(0, "end")
                        entry.insert(0, new_text)
                    else:
                        # Вставляем в позицию курсора
                        current = entry.get()
                        new_text = current[:cursor_pos] + clean_text + current[cursor_pos:]
                        entry.delete(0, "end")
                        entry.insert(0, new_text)
                    
                    print(f"✅ Текст вставлен. Новая длина: {len(entry.get())}")
                    
                    if self.notifier:
                        self.notifier.show_success(f"📋 Вставлено {len(clean_text)} символов")
                else:
                    print("⚠️ Буфер обмена пуст")
                    
            except tk.TclError as e:
                print(f"❌ Ошибка доступа к буферу обмена: {e}")
                if self.notifier:
                    self.notifier.show_error("❌ Буфер обмена недоступен")
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")
                if self.notifier:
                    self.notifier.show_error(f"❌ Ошибка вставки")
            
            print(f"🔍 ===== КОНЕЦ =====\n")
            return "break"
        
        # Привязываем обработчик
        entry.bind('<Control-v>', on_paste)
        entry.bind('<Control-V>', on_paste)
        entry.bind('<Command-v>', on_paste)
        entry.bind('<Command-V>', on_paste)
        entry.bind('<Shift-Insert>', on_paste)
        
        print(f"✅ Привязан Ctrl+V к {field_name}")
        return entry
    
    def bind_paste_to_entries(self, entries_dict):
        """
        Привязывает Ctrl+V к словарю полей ввода
        
        Args:
            entries_dict: словарь вида {'имя_поля': виджет}
        """
        for field_name, entry in entries_dict.items():
            if entry:
                self.bind_paste_to_entry(entry, field_name)