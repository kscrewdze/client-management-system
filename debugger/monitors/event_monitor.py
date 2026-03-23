# -*- coding: utf-8 -*-

"""Мониторинг событий приложения"""
import threading
from datetime import datetime


class EventMonitor(threading.Thread):
    """Монитор событий"""
    
    def __init__(self, message_queue):
        super().__init__(daemon=True)
        self.message_queue = message_queue
        self.running = True
        self.events = []
        self.event_count = 0
    
    def run(self):
        """Запуск мониторинга"""
        self._log("🔄 Мониторинг событий запущен")
        while self.running:
            # Здесь можно добавить периодические проверки
            threading.Event().wait(1.0)
    
    def _log(self, message):
        """Внутренний метод для логирования"""
        try:
            self.message_queue.put({
                'time': datetime.now(),
                'level': 'EVENT',
                'message': message,
                'source': 'event'
            })
        except:
            pass
    
    def log_event(self, event_type, details):
        """Логирование события"""
        self.event_count += 1
        event = {
            'time': datetime.now(),
            'type': event_type,
            'details': details
        }
        self.events.append(event)
        self._log(f"Событие: {event_type} - {details}")
    
    def log_key_press(self, key, widget):
        """Логирование нажатия клавиши"""
        self.log_event('key_press', f"Клавиша: {key}, Виджет: {widget}")
    
    def log_focus_change(self, old, new):
        """Логирование смены фокуса"""
        self.log_event('focus_change', f"Фокус: {old} -> {new}")
    
    def log_window_event(self, event):
        """Логирование события окна"""
        self.log_event('window', event)
    
    def stop(self):
        """Остановка монитора"""
        self.running = False
        self._log("🛑 Мониторинг событий остановлен")
    
    def get_stats(self):
        """Получить статистику"""
        return {
            'total_events': self.event_count,
            'recent_events': self.events[-10:] if self.events else []
        }