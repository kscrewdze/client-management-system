# -*- coding: utf-8 -*-

"""Отладка вставки текста для диалогов"""
import tkinter as tk
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DebugPasteManager:
    """Класс для отладки вставки текста в диалогах"""
    
    def __init__(self, dialog, notifier=None, debug=True):
        """
        Инициализация менеджера отладки вставки
        
        Args:
            dialog: диалоговое окно
            notifier: объект для уведомлений
            debug: режим отладки
        """
        self.dialog = dialog
        self.notifier = notifier
        self.debug = debug
        self.log_file = None
        
        if debug:
            self.setup_logging()
        
        print("✅ DebugPasteManager инициализирован")
        self.log("Менеджер вставки запущен")
    
    def setup_logging(self):
        """Настройка логирования в файл"""
        try:
            import os
            from pathlib import Path
            
            # Логи сохраняем в корневую папку logs
            base_dir = Path(__file__).parent.parent.parent.parent
            log_dir = base_dir / "logs"
            log_dir.mkdir(exist_ok=True)
            
            self.log_file = log_dir / f"paste_debug_{datetime.now().strftime('%Y%m%d')}.log"
            self.log(f"Лог-файл: {self.log_file}")
        except Exception as e:
            print(f"❌ Ошибка настройки логирования: {e}")
    
    def log(self, message):
        """Запись в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_message + "\n")
            except Exception as e:
                print(f"❌ Ошибка записи в лог: {e}")
    
    def bind_paste_to_entry(self, entry, field_name):
        """Привязывает Ctrl+V к полю ввода с отладкой"""
        
        def on_paste(event):
            """Обработчик вставки текста с подробной отладкой"""
            self.log(f"\n{'='*60}")
            self.log(f"🔍 СОБЫТИЕ ВСТАВКИ В {field_name}")
            
            # Подробная информация о событии
            self.log(f"📌 Тип события: {event.type}")
            self.log(f"📌 Виджет: {event.widget}")
            self.log(f"📌 Класс виджета: {event.widget.__class__.__name__}")
            self.log(f"📌 Код клавиши: {event.keysym}")
            self.log(f"📌 Код символа: {event.keycode}")
            self.log(f"📌 Модификаторы: {event.state}")
            self.log(f"📌 X: {event.x}, Y: {event.y}")
            
            # Проверяем, есть ли фокус у виджета
            focused = self.dialog.focus_get()
            self.log(f"📌 Текущий фокус: {focused}")
            self.log(f"📌 Виджет в фокусе? {focused == entry}")
            
            # Пробуем получить текст из буфера обмена
            clipboard_text = None
            
            # Способ 1: через event.widget
            try:
                self.log("📋 Попытка 1: event.widget.clipboard_get()")
                clipboard_text = event.widget.clipboard_get()
                self.log(f"✅ Успех! Длина: {len(clipboard_text)}")
            except Exception as e:
                self.log(f"❌ Ошибка: {e}")
            
            # Способ 2: через self.dialog
            if not clipboard_text:
                try:
                    self.log("📋 Попытка 2: self.dialog.clipboard_get()")
                    clipboard_text = self.dialog.clipboard_get()
                    self.log(f"✅ Успех! Длина: {len(clipboard_text)}")
                except Exception as e:
                    self.log(f"❌ Ошибка: {e}")
            
            # Способ 3: через корневое окно
            if not clipboard_text:
                try:
                    self.log("📋 Попытка 3: корневое окно")
                    root = self.dialog.winfo_toplevel()
                    clipboard_text = root.clipboard_get()
                    self.log(f"✅ Успех! Длина: {len(clipboard_text)}")
                except Exception as e:
                    self.log(f"❌ Ошибка: {e}")
            
            if clipboard_text:
                # Показываем первые 50 символов
                preview = clipboard_text[:50].replace('\n', ' ').replace('\r', '')
                self.log(f"📋 Текст: '{preview}...'")
                
                # Очищаем текст (убираем лишние пробелы и переносы)
                clean_text = ' '.join(clipboard_text.split())
                self.log(f"🧹 Очищенный: '{clean_text[:50]}...'")
                
                # Получаем текущее содержимое
                try:
                    current = entry.get()
                    cursor_pos = entry.index("insert")
                    self.log(f"📍 Текущий текст ({len(current)}): '{current[:30]}...'")
                    self.log(f"📍 Позиция курсора: {cursor_pos}")
                    
                    # Вставляем текст
                    if cursor_pos == "end" or not isinstance(cursor_pos, int):
                        new_text = current + clean_text
                        self.log("📌 Вставка в конец")
                    else:
                        new_text = current[:cursor_pos] + clean_text + current[cursor_pos:]
                        self.log(f"📌 Вставка в позицию {cursor_pos}")
                    
                    # Обновляем поле
                    entry.delete(0, "end")
                    entry.insert(0, new_text)
                    
                    self.log(f"✅ Новый текст ({len(new_text)}): '{new_text[:30]}...'")
                    
                    if self.notifier:
                        self.notifier.show_success(f"📋 Вставлено {len(clean_text)} символов")
                    
                except Exception as e:
                    self.log(f"❌ Ошибка вставки: {e}")
                    import traceback
                    self.log(traceback.format_exc())
            else:
                self.log("⚠️ Не удалось получить текст из буфера обмена")
            
            self.log(f"{'='*60}\n")
            return "break"
        
        # Привязываем обработчик ВСЕМИ возможными способами
        entry.bind('<Control-v>', on_paste)
        entry.bind('<Control-V>', on_paste)
        entry.bind('<Control-Key-v>', on_paste)
        entry.bind('<Control-Key-V>', on_paste)
        
        # Для macOS
        entry.bind('<Command-v>', on_paste)
        entry.bind('<Command-V>', on_paste)
        
        # Альтернативный способ
        entry.bind('<Shift-Insert>', on_paste)
        
        # Привязываем также на уровне виджета
        entry.bind_class('Entry', '<Control-v>', on_paste)
        entry.bind_class('Entry', '<Control-V>', on_paste)
        
        self.log(f"✅ Привязан Ctrl+V к {field_name}")
        return entry
    
    def bind_paste_to_entries(self, entries_dict):
        """
        Привязывает Ctrl+V к словарю полей ввода
        
        Args:
            entries_dict: словарь вида {'имя_поля': виджет}
        """
        self.log(f"\n📋 Привязка вставки к {len(entries_dict)} полям")
        for field_name, entry in entries_dict.items():
            if entry:
                self.bind_paste_to_entry(entry, field_name)
        
        self.log("✅ Все поля привязаны")
    
    def test_clipboard(self):
        """Тестирование доступа к буферу обмена"""
        self.log("\n🔍 ТЕСТИРОВАНИЕ БУФЕРА ОБМЕНА")
        try:
            clipboard = self.dialog.clipboard_get()
            preview = clipboard[:100].replace('\n', ' ').replace('\r', '')
            self.log(f"✅ Буфер обмена доступен")
            self.log(f"📋 Содержит ({len(clipboard)} символов): '{preview}...'")
            return True
        except Exception as e:
            self.log(f"❌ Буфер обмена недоступен: {e}")
            return False