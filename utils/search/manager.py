# -*- coding: utf-8 -*-

"""Основной класс для поиска клиентов"""
from typing import List, Optional, Callable
import logging
from database import Database

from utils.search.history import history_manager
from utils.search.filters import filters
from utils.search.exporters import exporter
from utils.search.highlight import highlighter

logger = logging.getLogger(__name__)


class ClientSearch:
    """Класс для управления поиском клиентов"""
    
    def __init__(self, db, notifier=None):
        """
        Инициализация поиска
        
        Args:
            db: объект базы данных
            notifier: объект для уведомлений
        """
        self.db = db
        self.notifier = notifier
        self.last_query = ""       # Последний запрос
        self.last_results = []     # Последние результаты
        self.search_delay = 500    # Задержка поиска в мс
        self.after_id = None       # ID для after()
        self.last_master = None    # Последний master для after
        
        print("✅ ClientSearch инициализирован")
    
    def search(self, query: str, callback: Optional[Callable] = None) -> List:
        """
        Поиск клиентов по запросу
        
        Args:
            query: строка поиска
            callback: функция для вызова с результатами
            
        Returns:
            List: список найденных клиентов
        """
        # Если запрос пустой или меньше 4 символов - возвращаем всех
        if not query or len(query.strip()) < 4:
            print(f"📋 Запрос '{query}' слишком короткий (мин. 4 символа), показываем всех клиентов")
            results = self.db.get_all_clients()
            self.last_query = ""
            self.last_results = results
            
            if callback:
                callback(results)
            
            return results
        
        # Очищаем запрос
        clean_query = query.strip().lower()
        
        print(f"🔍 Поиск: '{clean_query}'")
        
        # Добавляем в историю
        history_manager.add(clean_query)
        
        # Выполняем поиск
        try:
            # Используем метод search_clients из базы данных
            results = self.db.search_clients(clean_query)
            
            # Дополнительная отладка
            print(f"📊 Получено результатов: {len(results)}")
            if len(results) > 0:
                print(f"   Первый клиент: {results[0].name}")
            else:
                print("   Нет результатов")
            
            self.last_query = clean_query
            self.last_results = results
            
            # Показываем уведомление
            if self.notifier:
                if len(results) == 0:
                    self.notifier.show_info(f"🔍 Ничего не найдено")
                else:
                    self.notifier.show_success(f"🔍 Найдено {len(results)}")
            
            # Вызываем callback если есть
            if callback:
                callback(results)
            
            return results
            
        except Exception as e:
            error_msg = f"❌ Ошибка поиска: {e}"
            print(error_msg)
            logger.error(error_msg, exc_info=True)
            
            if self.notifier:
                self.notifier.show_error("❌ Ошибка при поиске")
            
            return []
    
    def delayed_search(self, query: str, callback: Callable, delay: int = None, master=None):
        """
        Поиск с задержкой (использует after вместо потоков)
        
        Args:
            query: строка поиска
            callback: функция для вызова с результатами
            delay: задержка в мс
            master: родительский виджет для after()
        """
        # Если нет master, ищем его
        if master is None and hasattr(self, 'last_master'):
            master = self.last_master
        
        if master is None:
            # Если нет master, выполняем сразу
            print("⚠️ Нет master для after, выполняем сразу")
            results = self.search(query)
            if callback:
                callback(results)
            return
        
        # Сохраняем master для будущих вызовов
        self.last_master = master
        
        # Отменяем предыдущий after
        if self.after_id:
            try:
                master.after_cancel(self.after_id)
            except:
                pass
            self.after_id = None
        
        # Если запрос слишком короткий, сразу показываем всех
        if len(query.strip()) < 4:
            callback(self.db.get_all_clients())
            return
        
        # Устанавливаем новую задержку
        delay = delay or self.search_delay
        
        # Используем after вместо threading
        self.after_id = master.after(delay, lambda: self._execute_search(query, callback, master))
        
        print(f"⏱ Поиск через {delay}мс: '{query}'")
    
    def _execute_search(self, query: str, callback: Callable, master):
        """Выполнение отложенного поиска"""
        try:
            # Выполняем поиск в основном потоке
            results = self.search(query)
            if callback:
                # Используем after для callback
                master.after(0, lambda: callback(results))
        except Exception as e:
            print(f"❌ Ошибка отложенного поиска: {e}")
        finally:
            self.after_id = None
    
    # Делегирование методов другим классам
    @property
    def history(self):
        """Доступ к истории поиска"""
        return history_manager
    
    @property
    def filters(self):
        """Доступ к фильтрам"""
        return filters
    
    @property
    def exporter(self):
        """Доступ к экспортерам"""
        return exporter
    
    @property
    def highlighter(self):
        """Доступ к подсветке"""
        return highlighter
    
    def get_search_history(self) -> List[str]:
        """Получить историю поиска"""
        return history_manager.get_all()
    
    def clear_history(self):
        """Очистить историю поиска"""
        history_manager.clear()
    
    def get_last_results(self) -> List:
        """Получить последние результаты поиска"""
        return self.last_results.copy()
    
    def get_last_query(self) -> str:
        """Получить последний запрос"""
        return self.last_query
    
    def export_results(self, clients: List, format: str = "txt") -> str:
        """
        Экспорт результатов поиска
        
        Args:
            clients: список клиентов
            format: формат экспорта (txt, csv, json, html)
            
        Returns:
            str: отформатированный текст
        """
        if format == "csv":
            return exporter.to_csv(clients)
        elif format == "json":
            return exporter.to_json(clients)
        elif format == "html":
            return exporter.to_html(clients)
        else:  # txt
            return exporter.to_txt(clients)
    
    def highlight_results(self, clients: List, query: str) -> List[dict]:
        """
        Подсветка результатов поиска
        
        Args:
            clients: список клиентов
            query: поисковый запрос
            
        Returns:
            List[dict]: список словарей с подсвеченными полями
        """
        return highlighter.highlight_in_list(clients, query)


# Создаем глобальный экземпляр
search_manager = None


def init_search(db, notifier=None):
    """Инициализация глобального менеджера поиска"""
    global search_manager
    search_manager = ClientSearch(db, notifier)
    return search_manager


def get_search() -> ClientSearch:
    """Получить глобальный менеджер поиска"""
    global search_manager
    if search_manager is None:
        raise ValueError("Search manager not initialized. Call init_search first.")
    return search_manager