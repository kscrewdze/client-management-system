# -*- coding: utf-8 -*-

"""Информационная секция для экспорта"""
import os
from datetime import datetime  # ДОБАВЛЕН ИМПОРТ
import customtkinter as ctk
from widgets.tooltip import ToolTip
from config.settings import Settings


class InfoSection:
    """Класс для информационной секции"""
    
    def __init__(self, parent, notifier):
        self.parent = parent
        self.notifier = notifier
        self.export_dir = Settings.EXPORTS_DIR
        self.folder_label = None
        self.stats_label = None
        self.update_after_id = None
        self.is_running = True
    
    def create(self):
        """Создание информационной секции"""
        info_frame = ctk.CTkFrame(self.parent, fg_color="#f0f0f0", corner_radius=8)
        info_frame.pack(fill="x", padx=40, pady=10)
        
        # Заголовок секции
        section_title = ctk.CTkLabel(
            info_frame,
            text="📁 ИНФОРМАЦИЯ ОБ ЭКСПОРТЕ",
            font=("Segoe UI", 12, "bold"),
            text_color="#2b5e8c"
        )
        section_title.pack(pady=(6, 2))
        
        # Разделитель
        separator = ctk.CTkFrame(info_frame, height=1, fg_color="#cccccc")
        separator.pack(fill="x", padx=15, pady=2)
        
        # Контейнер для информации
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=5)
        
        # Левая колонка - папка
        self._create_folder_info(details_frame)
        
        # Правая колонка - статистика
        self._create_stats_info(details_frame)
        
        # Кнопка открытия папки
        self._create_open_button(info_frame)
        
        # Подсказка
        hint_label = ctk.CTkLabel(
            info_frame,
            text="💡 Статистика обновляется автоматически",
            font=("Segoe UI", 8),
            text_color="gray"
        )
        hint_label.pack(pady=(0, 5))
        
        # Запускаем автообновление
        self.start_auto_update()
        
        # Первое обновление
        self.update_stats()
    
    def _create_folder_info(self, parent):
        """Создание информации о папке"""
        left_col = ctk.CTkFrame(parent, fg_color="transparent")
        left_col.pack(side="left", fill="x", expand=True)
        
        folder_row = ctk.CTkFrame(left_col, fg_color="transparent")
        folder_row.pack(anchor="w", pady=2)
        
        folder_icon = ctk.CTkLabel(
            folder_row,
            text="📂",
            font=("Segoe UI", 11)
        )
        folder_icon.pack(side="left", padx=(0, 5))
        
        folder_text = ctk.CTkLabel(
            folder_row,
            text="Папка:",
            font=("Segoe UI", 10, "bold"),
            text_color="#333333"
        )
        folder_text.pack(side="left")
        
        self.folder_label = ctk.CTkLabel(
            folder_row,
            text="",
            font=("Segoe UI", 9),
            text_color="#555555"
        )
        self.folder_label.pack(side="left", padx=(5, 0))
    
    def _create_stats_info(self, parent):
        """Создание информации о статистике"""
        right_col = ctk.CTkFrame(parent, fg_color="transparent")
        right_col.pack(side="right", fill="x", expand=True)
        
        stats_row = ctk.CTkFrame(right_col, fg_color="transparent")
        stats_row.pack(anchor="e", pady=2)
        
        stats_icon = ctk.CTkLabel(
            stats_row,
            text="📊",
            font=("Segoe UI", 11)
        )
        stats_icon.pack(side="left", padx=(0, 5))
        
        self.stats_label = ctk.CTkLabel(
            stats_row,
            text="загрузка...",
            font=("Segoe UI", 9),
            text_color="#555555"
        )
        self.stats_label.pack(side="left")
    
    def _create_open_button(self, parent):
        """Создание кнопки открытия папки"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(pady=5)
        
        open_btn = ctk.CTkButton(
            button_frame,
            text="📁 ОТКРЫТЬ ПАПКУ",
            command=self.open_export_folder,
            width=160,
            height=28,
            font=("Segoe UI", 10, "bold"),
            fg_color="#4a6fa5",
            hover_color="#3a5a8c",
            corner_radius=6
        )
        open_btn.pack()
        
        ToolTip(open_btn, "Открыть папку с экспортированными файлами")
    
    def start_auto_update(self):
        """Запуск автоматического обновления"""
        if self.is_running:
            self.update_stats()
            if hasattr(self, 'folder_label') and self.folder_label:
                self.update_after_id = self.folder_label.after(2000, self.start_auto_update)
    
    def stop_auto_update(self):
        """Остановка автоматического обновления"""
        self.is_running = False
        if self.update_after_id:
            try:
                if hasattr(self, 'folder_label') and self.folder_label:
                    self.folder_label.after_cancel(self.update_after_id)
            except:
                pass
            self.update_after_id = None
    
    def update_stats(self):
        """Обновление статистики экспорта"""
        try:
            if self.export_dir.exists():
                excel_files = list(self.export_dir.glob("*.xlsx"))
                json_files = list(self.export_dir.glob("*.json"))
                
                # Сортируем по дате создания (новые сверху)
                excel_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                excel_count = len(excel_files)
                json_count = len(json_files)
                total_files = excel_count + json_count
                
                # Формируем статистику
                stats_text = f"Всего: {total_files}"
                stats_parts = []
                
                if excel_count > 0:
                    stats_parts.append(f"Excel: {excel_count}")
                if json_count > 0:
                    stats_parts.append(f"JSON: {json_count}")
                
                if stats_parts:
                    stats_text += f" ({', '.join(stats_parts)})"
                
                # Добавляем информацию о последнем файле
                all_files = []
                for f in excel_files[:1] + json_files[:1]:
                    if f:
                        all_files.append(f)
                
                if all_files:
                    latest = max(all_files, key=lambda x: x.stat().st_mtime)
                    time_str = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%H:%M:%S")
                    stats_text += f"\nПоследний: {latest.name} ({time_str})"
                
                if self.stats_label:
                    self.stats_label.configure(text=stats_text)
                
                # Обновляем путь
                folder_path = str(self.export_dir)
                if len(folder_path) > 40:
                    folder_path = "..." + folder_path[-40:]
                if self.folder_label:
                    self.folder_label.configure(text=folder_path)
            else:
                if self.stats_label:
                    self.stats_label.configure(text="Папка еще не создана")
        except Exception as e:
            if self.stats_label:
                self.stats_label.configure(text=f"Ошибка: {str(e)[:20]}")
    
    def open_export_folder(self):
        """Открытие папки с экспортами"""
        try:
            if not self.export_dir.exists():
                self.export_dir.mkdir(parents=True)
                self.notifier.show_info("📁 Папка создана")
            
            os.startfile(str(self.export_dir))
            self.notifier.show_success("📁 Папка открыта")
            self.update_stats()  # Мгновенное обновление
        except Exception as e:
            self.notifier.show_error(f"❌ Ошибка: {str(e)}")
    
    def cancel_updates(self):
        """Отмена обновлений при закрытии"""
        self.stop_auto_update()