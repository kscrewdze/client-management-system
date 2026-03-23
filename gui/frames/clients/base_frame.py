# -*- coding: utf-8 -*-

"""Базовый фрейм со списком клиентов"""
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import logging

from database import Database
from widgets.notifications import NotificationLabel
from widgets.tooltip import ToolTip
from utils.search import ClientSearch

# Импортируем компоненты
from gui.frames.clients.table_widget import TableWidget
from gui.frames.clients.search_widget import SearchWidget
from gui.frames.clients.actions import ClientActions
from gui.frames.clients.shortcuts import Shortcuts

logger = logging.getLogger(__name__)


class ClientsListFrame(ctk.CTkFrame):
    """Фрейм со списком клиентов"""
    
    def __init__(self, parent, db: Database, refresh_callback, notifier: NotificationLabel):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.refresh_callback = refresh_callback
        self.notifier = notifier
        self.selected_item = None
        self.tooltip = None
        self.search_info_label = None
        self.status_label = None
        self.search_entry = None  # Будет установлен позже
        
        # Инициализируем поиск
        self.search_manager = ClientSearch(db, notifier)
        
        # Создаем компоненты
        self.table_widget = TableWidget(self)
        self.search_widget = SearchWidget(self)
        self.actions = ClientActions(self)
        self.shortcuts = Shortcuts(self)
        
        self.create_widgets()
        self.shortcuts.bind_shortcuts()
        logger.info("Инициализация фрейма клиентов")
    
    def create_widgets(self):
        """Создание виджетов"""
        # Верхняя панель
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Заголовок
        title_label = ctk.CTkLabel(
            top_frame,
            text="📋 КЛИЕНТЫ",
            font=("Segoe UI", 18, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(side="left")
        
        # Панель поиска - получаем search_entry
        search_frame, self.search_entry = self.search_widget.create_search_frame(top_frame)
        search_frame.pack(side="right")
        
        # Панель кнопок
        buttons_frame = self.actions.create_buttons_frame()
        buttons_frame.pack(fill="x", pady=(10, 10))
        
        # Информационная строка
        info_label = ctk.CTkLabel(
            buttons_frame,
            text="👆 Наведите на имя для комментария | Двойной клик - копировать Telegram",
            font=("Segoe UI", 11),
            text_color="#666666"
        )
        info_label.pack(side="right", padx=10)
        
        # Информация о поиске
        self.search_info_label = ctk.CTkLabel(
            buttons_frame,
            text="",
            font=("Segoe UI", 11, "italic"),
            text_color="#0288d1"
        )
        self.search_info_label.pack(side="right", padx=10)
        
        # Таблица
        self.table_widget.create_table()
        
        # Статусная строка
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 11),
            text_color="gray"
        )
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        self.refresh()
    
    def refresh(self, clients=None):
        """Обновление списка клиентов"""
        self.table_widget.refresh(clients)
    
    def on_search_changed(self, *args):
        """Обработка изменения поискового запроса"""
        self.search_widget.on_search_changed(*args)
    
    def display_search_results(self, results):
        """Отображение результатов поиска"""
        self.search_widget.display_search_results(results)
    
    def show_advanced_search(self):
        """Показать расширенный поиск"""
        self.search_widget.show_advanced_search()
    
    def use_search_history(self, query, dialog):
        """Использовать запрос из истории"""
        self.search_widget.use_search_history(query, dialog)
    
    def clear_search_history(self):
        """Очистить историю поиска"""
        self.search_widget.clear_search_history()
    
    def clear_search(self):
        """Очистить поиск"""
        self.search_widget.clear_search()
    
    def on_tree_select(self, event):
        """Выбор элемента в дереве"""
        self.table_widget.on_tree_select(event)
    
    def on_tree_double_click(self, event):
        """Двойной клик - копирование Telegram"""
        self.table_widget.on_tree_double_click(event)
    
    def on_tree_motion(self, event):
        """Подсказка при наведении"""
        self.table_widget.on_tree_motion(event)
    
    def show_comment_tooltip(self, event, comment):
        """Показать подсказку с комментарием"""
        self.table_widget.show_comment_tooltip(event, comment)
    
    def hide_comment_tooltip(self, event=None):
        """Скрыть подсказку"""
        self.table_widget.hide_comment_tooltip(event)
    
    def get_selected_client_telegram(self):
        """Получить Telegram выбранного клиента"""
        return self.table_widget.get_selected_client_telegram()
    
    def get_selected_client_id(self):
        """Получить ID выбранного клиента"""
        return self.table_widget.get_selected_client_id()
    
    def copy_telegram(self):
        """Копировать Telegram в буфер обмена"""
        self.actions.copy_telegram()
    
    def toggle_completed(self):
        """Переключить статус выполнения"""
        self.actions.toggle_completed()
    
    def edit_selected(self):
        """Редактировать выбранного клиента"""
        self.actions.edit_selected()
    
    def delete_selected(self):
        """Удалить выбранного клиента"""
        self.actions.delete_selected()