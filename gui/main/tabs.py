# -*- coding: utf-8 -*-

"""Управление вкладками главного окна"""
import customtkinter as ctk

from gui.frames.statistics_frame import StatisticsFrame
from gui.frames.clients import ClientsListFrame
from gui.frames.matrices import MatricesFrame
from gui.frames.add_client import AddClientFrame
from gui.frames.export import ExportFrame
from gui.frames.settings import ThemesFrame


class TabsManager:
    """Класс для управления вкладками"""
    
    def __init__(self, parent, db, notifier, refresh_callback):
        self.parent = parent
        self.db = db
        self.notifier = notifier
        self.refresh_callback = refresh_callback
        self.notebook = None
        self.frames = {}
    
    def create(self):
        """Создание блокнота с вкладками"""
        self.notebook = ctk.CTkTabview(self.parent)
        
        # Фиксируем высоту вкладок
        self.notebook.pack(fill="both", expand=True, pady=(2, 0))
        
        # Настройка внешнего вида
        self.notebook._segmented_button.configure(
            height=32,
            corner_radius=0
        )
        
        self._create_all_tabs()
        
        return self.notebook
    
    def _create_all_tabs(self):
        """Создание всех вкладок"""
        # Вкладка статистики
        self.notebook.add("📊 Статистика")
        self.frames['statistics'] = StatisticsFrame(
            self.notebook.tab("📊 Статистика"),
            self.db,
            self.notifier
        )
        self._configure_tab_frame(self.frames['statistics'])
        
        # Вкладка клиентов
        self.notebook.add("📋 Клиенты")
        self.frames['clients'] = ClientsListFrame(
            self.notebook.tab("📋 Клиенты"),
            self.db,
            self.refresh_callback,
            self.notifier
        )
        self._configure_tab_frame(self.frames['clients'])
        
        # Вкладка матриц
        self.notebook.add("📊 Матрицы")
        self.frames['matrices'] = MatricesFrame(
            self.notebook.tab("📊 Матрицы"),
            self.db,
            self.notifier,
            self.refresh_callback
        )
        self._configure_tab_frame(self.frames['matrices'])
        
        # Вкладка добавления
        self.notebook.add("➕ Добавить")
        self.frames['add'] = AddClientFrame(
            self.notebook.tab("➕ Добавить"),
            self.db,
            self.refresh_callback,
            self.notifier
        )
        self._configure_tab_frame(self.frames['add'])
        
        # Вкладка экспорта
        self.notebook.add("📊 Экспорт")
        self.frames['export'] = ExportFrame(
            self.notebook.tab("📊 Экспорт"),
            self.db,
            self.notifier
        )
        self._configure_tab_frame(self.frames['export'])
        
        # Вкладка тем
        self.notebook.add("🎨 Темы")
        self.frames['themes'] = ThemesFrame(
            self.notebook.tab("🎨 Темы"),
            self.notifier,
            self.db
        )
        self._configure_tab_frame(self.frames['themes'])
    
    def _configure_tab_frame(self, frame):
        """Настройка фрейма вкладки"""
        frame.pack(fill="both", expand=True, padx=3, pady=3)
        frame.pack_propagate(False)
        frame.configure(height=500)
    
    def refresh_all(self):
        """Обновить данные во всех вкладках"""
        if 'clients' in self.frames:
            try:
                self.frames['clients'].refresh()
            except:
                pass
        if 'statistics' in self.frames:
            try:
                self.frames['statistics'].refresh()
            except:
                pass
        if 'matrices' in self.frames:
            try:
                self.frames['matrices'].refresh()
            except:
                pass
        if 'add' in self.frames:
            try:
                self.frames['add'].load_matrices()
            except:
                pass
    
    def get_frame(self, name):
        """Получить фрейм по имени"""
        return self.frames.get(name)
    
    def set_tab(self, tab_name):
        """Переключиться на вкладку по имени"""
        if self.notebook:
            self.notebook.set(tab_name)