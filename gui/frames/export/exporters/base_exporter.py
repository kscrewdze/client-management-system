# -*- coding: utf-8 -*-

"""Базовый класс для экспортеров"""
from datetime import datetime
from tkinter import messagebox
import os
from config.settings import Settings


class BaseExporter:
    """Базовый класс экспортера"""
    
    def __init__(self, db, notifier):
        """
        Инициализация базового экспортера
        
        Args:
            db: объект базы данных
            notifier: объект для уведомлений
        """
        self.db = db
        self.notifier = notifier
        self.export_dir = Settings.EXPORTS_DIR
    
    def get_export_filename(self, extension):
        """
        Генерация имени файла для экспорта
        
        Args:
            extension: расширение файла (без точки)
            
        Returns:
            Path: путь к файлу
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.export_dir / f"clients_export_{timestamp}.{extension}"
    
    def check_data(self):
        """
        Проверка наличия данных для экспорта
        
        Returns:
            list: список клиентов или None если нет данных
        """
        clients = self.db.get_all_clients()
        if not clients:
            self.notifier.show_warning("⚠️ Нет данных для экспорта")
            return None
        return clients
    
    def ask_open_folder(self, filename):
        """
        Спросить пользователя, открыть ли папку с экспортом
        
        Args:
            filename: имя сохраненного файла
            
        Returns:
            bool: True если пользователь хочет открыть папку
        """
        return messagebox.askyesno(
            "Успех", 
            f"Файл сохранен:\n{filename.name}\n\nОткрыть папку?"
        )
    
    def open_export_folder(self):
        """Открыть папку с экспортами"""
        try:
            if not self.export_dir.exists():
                self.export_dir.mkdir(parents=True)
            
            os.startfile(str(self.export_dir))
        except Exception as e:
            self.notifier.show_error(f"❌ Ошибка при открытии папки: {str(e)}")