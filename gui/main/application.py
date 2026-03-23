# -*- coding: utf-8 -*-

"""Главное окно приложения
Автор: kScrewdze
Версия: 9.0
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

from config.settings import Settings
from database import Database
from widgets.notifications import NotificationLabel
from themes import theme_manager
from utils.timer_manager import timer_manager

from gui.main.header import Header
from gui.main.status_bar import StatusBar
from gui.main.tabs import TabsManager
from gui.main.shortcuts import Shortcuts


class MainApplication:
    """Главный класс приложения"""
    
    def __init__(self):
        # Создание корневого окна
        self.root = ctk.CTk()
        self.root.title(Settings.APP_TITLE)
        self.root.geometry("1000x600")
        self.root.minsize(900, 550)
        
        # Привязка F12 для открытия отладчика
        self.root.bind('<F12>', lambda e: self.toggle_debugger())
        
        # Центрируем окно
        self.center_window()
        
        # ВАЖНО: сначала устанавливаем главное окно
        theme_manager.set_main_window(self.root)
        
        # Потом все остальное
        Settings.ensure_directories()
        self.db = Database()
        self.notifier = NotificationLabel(self.root)
        
        # Инициализация компонентов
        self.header = Header(self)
        self.tabs_manager = TabsManager(
            self.root, 
            self.db, 
            self.notifier, 
            self.refresh_data
        )
        self.status_bar = StatusBar(self.root, self.db.db_path)
        self.shortcuts = Shortcuts(
            self.root, 
            self.tabs_manager.notebook, 
            self.refresh_data
        )
        
        self.create_widgets()
        self.shortcuts.bind_all()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Проверка
        current = theme_manager.get_current_theme()
        if current:
            print(f"🎨 При запуске применена тема: {current.name}")
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = 1000
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создание виджетов главного окна"""
        # Основной контейнер
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Верхняя панель с заголовком
        self.header.create(main_container)
        
        # Блокнот с вкладками
        self.tabs_manager.create()
        
        # Строка состояния
        self.status_bar.create()
    
    def refresh_data(self):
        """Обновление данных во всех вкладках"""
        try:
            self.tabs_manager.refresh_all()
            self.status_bar.set_status("✅ Данные обновлены")
            self.notifier.show_success("✅ Данные обновлены")
        except Exception as e:
            self.status_bar.set_status(f"❌ Ошибка: {str(e)[:30]}")
            self.notifier.show_error(f"❌ Ошибка: {str(e)}")
    
    def on_closing(self):
        """Обработка закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            try:
                # Отменяем все таймеры
                timer_manager.cancel_all()
                
                # Отменяем обновления в header
                if hasattr(self, 'header'):
                    self.header.cancel_updates()
                
                # Закрываем соединение с БД
                self.db.close()
                
                # Уничтожаем окно
                self.root.quit()
                self.root.destroy()
            except Exception as e:
                print(f"⚠️ Ошибка при закрытии: {e}")
                # Принудительное закрытие
                try:
                    self.root.destroy()
                except:
                    pass
    
    def toggle_debugger(self):
        """Переключение отладчика"""
        try:
            from debugger import toggle_debugger
            toggle_debugger()
            print("🔍 Отладчик переключен")
        except ImportError as e:
            print(f"❌ Ошибка импорта отладчика: {e}")
            print("📁 Проверьте наличие папки debugger/ и файла __init__.py")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def run(self):
        """Запуск приложения"""
        try:
            self.root.mainloop()
        except tk.TclError as e:
            if "invalid command name" in str(e):
                # Игнорируем ошибки после закрытия
                pass
            else:
                raise