# -*- coding: utf-8 -*-

"""Виджет поиска клиентов"""
import customtkinter as ctk
from widgets.tooltip import ToolTip


class SearchWidget:
    """Класс для поиска клиентов"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.notifier = parent.notifier
        self.search_manager = parent.search_manager
        self.search_var = None
        self.search_entry = None
        self.clear_search_btn = None
        self.advanced_search_btn = None
    
    def create_search_frame(self, parent_frame):
        """Создание панели поиска"""
        search_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        
        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="🔍 Поиск...",
            width=150,
            height=32,
            font=("Segoe UI", 11)
        )
        self.search_entry.pack(side="left", padx=(0, 3))
        
        # Сохраняем ссылку в parent для доступа из других классов
        self.parent.search_entry = self.search_entry
        
        self.clear_search_btn = ctk.CTkButton(
            search_frame,
            text="✕",
            command=self.clear_search,
            width=32,
            height=32,
            font=("Segoe UI", 12, "bold"),
            fg_color="#757575",
            hover_color="#616161"
        )
        self.clear_search_btn.pack(side="left")
        ToolTip(self.clear_search_btn, "Очистить поиск")
        
        self.advanced_search_btn = ctk.CTkButton(
            search_frame,
            text="⚙️",
            command=self.show_advanced_search,
            width=32,
            height=32,
            font=("Segoe UI", 12, "bold"),
            fg_color="#9c27b0",
            hover_color="#7b1fa2"
        )
        self.advanced_search_btn.pack(side="left", padx=(3, 0))
        ToolTip(self.advanced_search_btn, "Расширенный поиск")
        
        return search_frame, self.search_entry
    
    def on_search_changed(self, *args):
        """Обработка изменения поискового запроса"""
        query = self.search_var.get().strip()
        
        # Ищем только от 4 символов (ИЗМЕНЕНО с 2 на 4)
        if len(query) < 4:
            self.parent.search_info_label.configure(text="")
            self.parent.refresh()
            return
        
        # Используем отложенный поиск с after
        self.search_manager.delayed_search(query, self.display_search_results, master=self.parent)
        self.parent.search_info_label.configure(text=f"🔍 Поиск: '{query}'")
    
    def display_search_results(self, results):
        """Отображение результатов поиска"""
        self.parent.refresh(results)
        
        # Показываем информацию о результатах
        query = self.search_manager.get_last_query()
        if query:
            count = len(results)
            if count > 0:
                self.parent.search_info_label.configure(text=f"🔍 Найдено: {count}")
            else:
                self.parent.search_info_label.configure(text=f"🔍 Ничего не найдено")
    
    def show_advanced_search(self):
        """Показать расширенный поиск"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("🔍 Расширенный поиск")
        dialog.geometry("400x400")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Заголовок
        title_label = ctk.CTkLabel(
            dialog, 
            text="🔍 Расширенный поиск", 
            font=("Segoe UI", 16, "bold"),
            text_color="#2b5e8c"
        )
        title_label.pack(pady=10)
        
        # Инструкция - ИЗМЕНЕНО с 2 на 4 символа
        info_label = ctk.CTkLabel(
            dialog,
            text="Поиск работает по имени, телефону и Telegram\nМинимум 4 символа",  # ИЗМЕНЕНО
            font=("Segoe UI", 11),
            text_color="gray"
        )
        info_label.pack(pady=(0, 10))
        
        # Кнопка очистки истории
        clear_history_btn = ctk.CTkButton(
            dialog,
            text="🗑 Очистить историю поиска",
            command=self.clear_search_history,
            width=200,
            height=35,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            font=("Segoe UI", 11, "bold")
        )
        clear_history_btn.pack(pady=5)
        
        # История поиска
        history_label = ctk.CTkLabel(
            dialog, 
            text="История поиска:", 
            font=("Segoe UI", 12, "bold")
        )
        history_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        # Фрейм для истории
        history_frame = ctk.CTkFrame(dialog)
        history_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Получаем историю
        history = self.search_manager.get_search_history()
        
        if history:
            # Показываем последние 5 запросов
            for i, query in enumerate(reversed(history[-5:])):
                btn = ctk.CTkButton(
                    history_frame,
                    text=query,
                    command=lambda q=query: self.use_search_history(q, dialog),
                    fg_color="transparent",
                    text_color="black",
                    hover_color="#e0e0e0",
                    anchor="w",
                    height=30
                )
                btn.pack(fill="x", padx=5, pady=1)
        else:
            empty_label = ctk.CTkLabel(
                history_frame, 
                text="История пуста", 
                text_color="gray",
                font=("Segoe UI", 11)
            )
            empty_label.pack(pady=20)
        
        # Кнопка закрытия
        close_btn = ctk.CTkButton(
            dialog,
            text="Закрыть",
            command=dialog.destroy,
            width=100,
            height=32,
            fg_color="#757575",
            hover_color="#616161"
        )
        close_btn.pack(pady=10)
    
    def use_search_history(self, query, dialog):
        """Использовать запрос из истории"""
        self.search_var.set(query)
        dialog.destroy()
    
    def clear_search_history(self):
        """Очистить историю поиска"""
        self.search_manager.clear_history()
        self.notifier.show_success("🗑 История поиска очищена")
        
        # Обновляем окно расширенного поиска если оно открыто
        for widget in self.parent.winfo_children():
            if isinstance(widget, ctk.CTkToplevel) and widget.title() == "🔍 Расширенный поиск":
                widget.destroy()
                self.parent.after(100, self.show_advanced_search)
                break
    
    def clear_search(self):
        """Очистить поиск"""
        self.search_var.set("")
        self.parent.search_info_label.configure(text="")
        self.parent.refresh()