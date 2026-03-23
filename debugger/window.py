# -*- coding: utf-8 -*-

"""Главное окно отладчика"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime
import threading
import queue

from debugger.monitors.clipboard_monitor import ClipboardMonitor
from debugger.monitors.event_monitor import EventMonitor
from debugger.monitors.shortcut_monitor import ShortcutMonitor
from debugger.monitors.database_monitor import DatabaseMonitor
from debugger.panels.log_panel import LogPanel
from debugger.panels.stats_panel import StatsPanel
from debugger.panels.test_panel import TestPanel
from debugger.storage.session_logger import SessionLogger


class DebuggerWindow:
    """Главное окно отладчика"""
    
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
        
        self.window = None
        self.notebook = None
        self.monitors = {}
        self.panels = {}
        self.message_queue = queue.Queue()
        self.running = True
        
        self.create_window()
        self.init_monitors()  # ВЫЗЫВАЕМ МЕТОД
        self.init_panels()
        self.start_monitors()
        self.process_queue()
        
        print("✅ DebuggerWindow инициализирован")
    
    def create_window(self):
        """Создание окна отладчика"""
        self.window = ctk.CTkToplevel()
        self.window.title("🔍 ОТЛАДЧИК")
        self.window.geometry("900x600")
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        
        # Настройка сетки
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=0)  # Заголовок
        self.window.grid_rowconfigure(1, weight=1)  # Основное содержимое
        self.window.grid_rowconfigure(2, weight=0)  # Статус бар
        
        # Заголовок
        self.create_header()
        
        # Блокнот с вкладками
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Статус бар
        self.create_status_bar()
        
        self.window.withdraw()  # Скрываем при запуске
    
    def create_header(self):
        """Создание заголовка"""
        header = ctk.CTkFrame(self.window, height=40, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="🔍 ОТЛАДЧИК ПРИЛОЖЕНИЯ",
            font=("Segoe UI", 16, "bold"),
            text_color="#d32f2f"
        )
        title.pack(side="left", padx=10)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=5)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Очистить логи",
            command=self.clear_all_logs,
            width=100,
            height=28,
            font=("Segoe UI", 11)
        )
        clear_btn.pack(side="left", padx=2)
        
        export_btn = ctk.CTkButton(
            btn_frame,
            text="Экспорт",
            command=self.export_logs,
            width=80,
            height=28,
            font=("Segoe UI", 11)
        )
        export_btn.pack(side="left", padx=2)
        
        close_btn = ctk.CTkButton(
            btn_frame,
            text="Скрыть",
            command=self.hide,
            width=80,
            height=28,
            font=("Segoe UI", 11)
        )
        close_btn.pack(side="left", padx=2)
    
    def create_status_bar(self):
        """Создание строки состояния"""
        status = ctk.CTkFrame(self.window, height=25, corner_radius=0, fg_color="#f0f0f0")
        status.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        status.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status,
            text="✅ Отладчик активен | F12 - показать/скрыть",
            font=("Segoe UI", 10),
            text_color="#555555"
        )
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(
            status,
            text="",
            font=("Segoe UI", 10),
            text_color="#555555"
        )
        self.time_label.pack(side="right", padx=10)
        
        self.update_time()
    
    def init_monitors(self):
        """Инициализация мониторов"""
        try:
            self.monitors['clipboard'] = ClipboardMonitor(self.message_queue)
            self.monitors['event'] = EventMonitor(self.message_queue)
            self.monitors['shortcut'] = ShortcutMonitor(self.message_queue)
            self.monitors['database'] = DatabaseMonitor(self.message_queue)
            
            self.log_message("✅ Все мониторы инициализированы")
        except Exception as e:
            self.log_message(f"❌ Ошибка инициализации мониторов: {e}")
    
    def init_panels(self):
        """Инициализация панелей"""
        self.panels['log'] = LogPanel(self.notebook, self.message_queue)
        self.panels['stats'] = StatsPanel(self.notebook, self.monitors)
        self.panels['test'] = TestPanel(self.notebook, self.monitors)
        
        self.notebook.add(self.panels['log'].frame, text="📋 Логи")
        self.notebook.add(self.panels['stats'].frame, text="📊 Статистика")
        self.notebook.add(self.panels['test'].frame, text="🧪 Тесты")
    
    def start_monitors(self):
        """Запуск мониторов"""
        for monitor in self.monitors.values():
            try:
                monitor.start()
            except Exception as e:
                self.log_message(f"❌ Ошибка запуска монитора: {e}")
    
    def stop_monitors(self):
        """Остановка мониторов"""
        self.running = False
        for monitor in self.monitors.values():
            try:
                monitor.stop()
            except Exception as e:
                print(f"⚠️ Ошибка остановки монитора: {e}")
    
    def process_queue(self):
        """Обработка очереди сообщений"""
        try:
            while True:
                msg = self.message_queue.get_nowait()
                if 'log' in self.panels:
                    self.panels['log'].add_message(msg)
        except queue.Empty:
            pass
        finally:
            if self.running and self.window:
                try:
                    self.window.after(100, self.process_queue)
                except:
                    pass
    
    def show(self):
        """Показать окно"""
        if self.window:
            try:
                self.window.deiconify()
                self.window.lift()
                self.log_message("🔍 Окно отладчика открыто")
            except:
                pass
    
    def hide(self):
        """Скрыть окно"""
        if self.window:
            try:
                self.window.withdraw()
            except:
                pass
    
    def toggle(self):
        """Переключить видимость окна"""
        if not self.window:
            return
        try:
            if self.window.state() == 'normal':
                self.hide()
            else:
                self.show()
        except:
            self.show()
    
    def log_message(self, message, level="INFO"):
        """Добавить сообщение в лог"""
        if 'log' in self.panels:
            self.panels['log'].add_message({
                'time': datetime.now(),
                'level': level,
                'message': message,
                'source': 'debugger'
            })
    
    def clear_all_logs(self):
        """Очистить все логи"""
        if 'log' in self.panels:
            self.panels['log'].clear()
            self.log_message("🧹 Логи очищены")
    
    def export_logs(self):
        """Экспорт логов"""
        try:
            from debugger.storage.export import export_logs
            if 'log' in self.panels:
                filename = export_logs(self.panels['log'].get_all())
                self.log_message(f"📁 Логи экспортированы в {filename}")
        except Exception as e:
            self.log_message(f"❌ Ошибка экспорта: {e}")
    
    def update_time(self):
        """Обновление времени"""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"🕐 {now}")
        if self.window:
            try:
                self.window.after(1000, self.update_time)
            except:
                pass


# Глобальный экземпляр
debugger = DebuggerWindow()


def show_debugger():
    """Показать отладчик"""
    debugger.show()


def hide_debugger():
    """Скрыть отладчик"""
    debugger.hide()


def toggle_debugger():
    """Переключить отладчик"""
    debugger.toggle()