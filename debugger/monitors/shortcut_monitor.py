# -*- coding: utf-8 -*-

"""Мониторинг горячих клавиш"""
import threading
from datetime import datetime


class ShortcutMonitor(threading.Thread):
    """Монитор горячих клавиш"""
    
    def __init__(self, message_queue):
        super().__init__(daemon=True)
        self.message_queue = message_queue
        self.running = True
        self.shortcuts = {}
        self.used_count = 0
    
    def run(self):
        """Запуск мониторинга"""
        self._log("🔄 Мониторинг горячих клавиш запущен")
        while self.running:
            threading.Event().wait(1.0)
    
    def _log(self, message):
        """Внутренний метод для логирования"""
        try:
            self.message_queue.put({
                'time': datetime.now(),
                'level': 'SHORTCUT',
                'message': message,
                'source': 'shortcut'
            })
        except:
            pass
    
    def register_shortcut(self, shortcut, description, widget):
        """Регистрация горячей клавиши"""
        self.shortcuts[shortcut] = {
            'description': description,
            'widget': widget,
            'registered_at': datetime.now()
        }
        self._log(f"📌 Зарегистрирована клавиша: {shortcut} - {description}")
    
    def log_shortcut_use(self, shortcut):
        """Логирование использования горячей клавиши"""
        self.used_count += 1
        desc = self.shortcuts.get(shortcut, {}).get('description', 'Неизвестно')
        self._log(f"⌨️ Использована клавиша: {shortcut} - {desc}")
    
    def stop(self):
        """Остановка монитора"""
        self.running = False
        self._log("🛑 Мониторинг горячих клавиш остановлен")
    
    def get_stats(self):
        """Получить статистику"""
        return {
            'registered': len(self.shortcuts),
            'used': self.used_count,
            'shortcuts': self.shortcuts
        }