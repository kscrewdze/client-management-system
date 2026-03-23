# -*- coding: utf-8 -*-

"""Менеджер таймеров для предотвращения ошибок after"""
import weakref


class TimerManager:
    """Глобальный менеджер для отслеживания и отмены таймеров"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._timers = []  # Используем обычный список вместо WeakSet
        self._counter = 0
    
    def register(self, after_id):
        """Зарегистрировать таймер"""
        if after_id:
            # Преобразуем в число, если это строка
            if isinstance(after_id, str):
                try:
                    after_id = int(float(after_id))
                except:
                    pass
            
            # Добавляем в список
            self._timers.append(after_id)
            self._counter += 1
            # print(f"⏱ Таймер {after_id} зарегистрирован (всего: {len(self._timers)})")
        return after_id
    
    def cancel(self, after_id):
        """Отменить конкретный таймер"""
        if after_id:
            try:
                # Преобразуем в число, если это строка
                if isinstance(after_id, str):
                    try:
                        after_id = int(float(after_id))
                    except:
                        pass
                
                # Пытаемся отменить
                if after_id in self._timers:
                    self._timers.remove(after_id)
                    # print(f"⏱ Таймер {after_id} отменен")
                    return True
            except:
                pass
        return False
    
    def cancel_all(self):
        """Отменить все зарегистрированные таймеры"""
        count = len(self._timers)
        self._timers.clear()
        print(f"⏱ Отменено {count} таймеров")
        return count
    
    def get_count(self):
        """Получить количество активных таймеров"""
        return len(self._timers)


# Глобальный экземпляр
timer_manager = TimerManager()