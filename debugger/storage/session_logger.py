# -*- coding: utf-8 -*-

"""Логирование сессии"""
import json
import os
from datetime import datetime


class SessionLogger:
    """Логгер сессии"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "sessions")
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"session_{self.session_id}.json")
        self.session_data = {
            'session_id': self.session_id,
            'start_time': datetime.now().isoformat(),
            'events': [],
            'stats': {}
        }
    
    def log_event(self, event_type, data):
        """Логирование события"""
        self.session_data['events'].append({
            'time': datetime.now().isoformat(),
            'type': event_type,
            'data': data
        })
        self.save()
    
    def update_stats(self, stats):
        """Обновление статистики"""
        self.session_data['stats'].update(stats)
        self.save()
    
    def save(self):
        """Сохранение сессии"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения сессии: {e}")
    
    def end_session(self):
        """Завершение сессии"""
        self.session_data['end_time'] = datetime.now().isoformat()
        self.save()
        return self.log_file


# Глобальный экземпляр
session_logger = SessionLogger()