# -*- coding: utf-8 -*-

"""Секция с темами"""
import customtkinter as ctk
from widgets.tooltip import ToolTip
from themes import theme_manager
from gui.dialogs.theme_dialog import ThemeDialog


class ThemesSection:
    """Секция выбора темы"""
    
    def __init__(self, parent, notifier):
        self.parent = parent
        self.notifier = notifier
        self.current_value = None
        self.theme_card = None
    
    def create_centered(self, parent_frame):
        """Создание центрированной карточки с темами"""
        # Карточка темы по центру
        self.theme_card = ctk.CTkFrame(
            parent_frame,
            width=500,
            height=400,
            corner_radius=20,
            fg_color="transparent"
        )
        self.theme_card.pack(expand=True, fill="both")
        self.theme_card.pack_propagate(False)
        
        self.create_content()
        
        return self.theme_card
    
    def create_content(self):
        """Создание содержимого карточки"""
        # Очищаем карточку
        for widget in self.theme_card.winfo_children():
            widget.destroy()
        
        # Иконка (кликабельная)
        icon_label = ctk.CTkLabel(
            self.theme_card,
            text="🎨",
            font=("Segoe UI", 80),
            cursor="hand2"
        )
        icon_label.pack(pady=(40, 10))
        icon_label.bind("<Button-1>", lambda e: self.show_theme_dialog())
        ToolTip(icon_label, "Кликните чтобы выбрать тему")
        
        # Заголовок (кликабельный)
        title_label = ctk.CTkLabel(
            self.theme_card,
            text="ОФОРМЛЕНИЕ",
            font=("Segoe UI", 28, "bold"),
            text_color="#2b5e8c",
            cursor="hand2"
        )
        title_label.pack(pady=(0, 20))
        title_label.bind("<Button-1>", lambda e: self.show_theme_dialog())
        ToolTip(title_label, "Кликните чтобы выбрать тему")
        
        # Текущая тема
        current = theme_manager.get_current_theme()
        current_text = current.name if current else "Стандартная"
        
        current_frame = ctk.CTkFrame(self.theme_card, fg_color="transparent")
        current_frame.pack(pady=15)
        
        current_label = ctk.CTkLabel(
            current_frame,
            text="Текущая тема:",
            font=("Segoe UI", 16)
        )
        current_label.pack(side="left")
        
        self.current_value = ctk.CTkLabel(
            current_frame,
            text=current_text,
            font=("Segoe UI", 16, "bold"),
            text_color="#2b5e8c"
        )
        self.current_value.pack(side="left", padx=(5, 0))
        
        # Подсказка (вместо кнопки)
        hint_frame = ctk.CTkFrame(self.theme_card, fg_color="transparent")
        hint_frame.pack(pady=30)
        
        hint_icon = ctk.CTkLabel(
            hint_frame,
            text="👇",
            font=("Segoe UI", 24)
        )
        hint_icon.pack()
        
        hint_label = ctk.CTkLabel(
            hint_frame,
            text="Кликните на иконку или название выше",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        hint_label.pack()
        
        # Список доступных тем (для информации)
        themes_list = ctk.CTkLabel(
            self.theme_card,
            text="Изумрудная • Сапфировая • Рубиновая •\nАметистовая • Полуночная • Рассветная",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        themes_list.pack(pady=5)
    
    def show_theme_dialog(self):
        """Показать диалог выбора темы"""
        dialog = ThemeDialog(self.parent.winfo_toplevel(), self.notifier)
        self.parent.wait_window(dialog.dialog)
        self.update_current_theme()
    
    def update_current_theme(self):
        """Обновить отображение текущей темы"""
        current = theme_manager.get_current_theme()
        if current:
            self.current_value.configure(text=current.name)