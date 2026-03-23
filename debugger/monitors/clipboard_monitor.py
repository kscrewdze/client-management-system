# -*- coding: utf-8 -*-

"""Мониторинг буфера обмена"""
import threading
import time
from datetime import datetime
import tkinter as tk


class ClipboardMonitor(threading.Thread):
    """Монитор буфера обмена"""
    
    def __init__(self, message_queue):
        super().__init__(daemon=True)
        self.message_queue = message_queue
        self.running = True
        self.last_content = ""
        self.check_count = 0
        self.paste_count = 0
    
    def run(self):
        """Запуск мониторинга"""
        self._log("🔄 Мониторинг буфера обмена запущен")
        while self.running:
            try:
                self.check_clipboard()
                time.sleep(1.0)
            except Exception as e:
                self._log(f"❌ Ошибка в мониторе: {e}")
    
    def _log(self, message):
        """Внутренний метод для логирования"""
        try:
            self.message_queue.put({
                'time': datetime.now(),
                'level': 'CLIPBOARD',
                'message': message,
                'source': 'clipboard'
            })
        except:
            pass
    
    def _get_clipboard_text(self):
        """Получение текста из буфера обмена"""
        temp_root = None
        try:
            temp_root = tk.Tk()
            temp_root.withdraw()
            text = temp_root.clipboard_get()
            return text
        except tk.TclError:
            return ""
        except Exception as e:
            self._log(f"⚠️ Ошибка получения текста: {e}")
            return ""
        finally:
            if temp_root:
                try:
                    temp_root.destroy()
                except:
                    pass
    
    def check_clipboard(self):
        """Проверка буфера обмена"""
        self.check_count += 1
        content = self._get_clipboard_text()
        
        if content and content != self.last_content:
            self.paste_count += 1
            self._log(f"📋 Изменение в буфере обмена #{self.paste_count}")
            self._log(f"   Длина: {len(content)} символов")
            preview = content[:100].replace('\n', ' ').replace('\r', '')
            self._log(f"   Первые 100: {preview}...")
            self.last_content = content
    
    def stop(self):
        """Остановка монитора"""
        self.running = False
        self._log(f"🛑 Мониторинг буфера обмена остановлен. Проверок: {self.check_count}, Вставок: {self.paste_count}")
    
    def get_stats(self):
        """Получить статистику"""
        return {
            'checks': self.check_count,
            'pastes': self.paste_count,
            'last_content': self.last_content[:100] if self.last_content else None
        }