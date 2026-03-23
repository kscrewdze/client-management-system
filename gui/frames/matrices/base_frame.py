# -*- coding: utf-8 -*-

"""Базовый фрейм для управления матрицами"""
import customtkinter as ctk
from database import Database
from widgets.notifications import NotificationLabel

from gui.frames.matrices.table_widget import MatrixTableWidget
from gui.frames.matrices.actions import MatrixActions


class MatricesFrame(ctk.CTkFrame):
    """Фрейм для управления матрицами"""
    
    def __init__(self, parent, db: Database, notifier: NotificationLabel, refresh_callback):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.notifier = notifier
        self.refresh_callback = refresh_callback
        
        # Инициализация компонентов
        self.table_widget = MatrixTableWidget(self)
        self.actions = MatrixActions(self)
        
        self.create_widgets()
        self.refresh()
        print("✅ MatricesFrame инициализирован")
    
    def create_widgets(self):
        """Создание виджетов"""
        # Панель инструментов
        self.actions.create_toolbar(self)
        
        # Таблица
        self.table_widget.create_table(self)
    
    def refresh(self):
        """Обновление списка матриц"""
        self.table_widget.refresh()
    
    def edit_selected(self):
        """Редактировать выбранную матрицу"""
        self.actions.edit_selected()