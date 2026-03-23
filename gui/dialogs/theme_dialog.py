# -*- coding: utf-8 -*-

"""Диалог выбора темы"""
import customtkinter as ctk
from gui.dialogs.base_dialog import BaseDialog
from gui.dialogs.styles import DialogStyles
from themes import theme_manager


class ThemeDialog(BaseDialog):
    """Диалог выбора темы оформления"""
    
    def __init__(self, parent, notifier):
        self.notifier = notifier
        super().__init__(parent, "🎨 Выбор темы", 500, 450)
        self.create_content()
        print("✅ ThemeDialog создан")
    
    def create_content(self):
        """Создание содержимого"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self.dialog,
            text="🎨 ВЫБОР ТЕМЫ",
            font=("Segoe UI", 20, "bold"),
            text_color=DialogStyles.COLOR_PRIMARY
        )
        title_label.pack(pady=(15, 5))
        
        # Описание
        desc_label = ctk.CTkLabel(
            self.dialog,
            text="Нажмите на тему, чтобы применить",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        desc_label.pack(pady=(0, 10))
        
        # Фрейм с темами (сетка 2x3)
        themes_grid = ctk.CTkFrame(self.dialog, fg_color="transparent")
        themes_grid.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Настройка сетки
        for i in range(2):
            themes_grid.grid_columnconfigure(i, weight=1, uniform="col")
        for i in range(3):
            themes_grid.grid_rowconfigure(i, weight=1, uniform="row")
        
        # Получаем все темы
        themes = theme_manager.get_all_themes()
        theme_list = list(themes.items())
        
        # Названия для отображения
        display_names = {
            "emerald": "Изумрудная",
            "sapphire": "Сапфировая",
            "ruby": "Рубиновая",
            "amethyst": "Аметистовая",
            "midnight": "Полуночная",
            "sunrise": "Рассветная"
        }
        
        # Цвета для превью
        theme_colors = {
            "emerald": ["#2e7d32", "#1b5e20", "#f1f8e9", "#1b5e20"],
            "sapphire": ["#0d47a1", "#1565c0", "#e3f2fd", "#0d47a1"],
            "ruby": ["#b71c1c", "#d32f2f", "#ffebee", "#b71c1c"],
            "amethyst": ["#4a148c", "#6a1b9a", "#f3e5f5", "#4a148c"],
            "midnight": ["#90caf9", "#64b5f6", "#121212", "#ffffff"],
            "sunrise": ["#ff6f00", "#ff8f00", "#fff3e0", "#bf360c"]
        }
        
        # Создаем карточки для каждой темы
        for i, (theme_name, theme_desc) in enumerate(theme_list):
            row = i // 2
            col = i % 2
            
            display_name = display_names.get(theme_name, theme_name.capitalize())
            colors = theme_colors.get(theme_name, ["#2b5e8c", "#1e3f5c", "#ffffff", "#000000"])
            
            self.create_theme_card(themes_grid, theme_name, display_name, colors, row, col)
    
    def create_theme_card(self, parent, theme_name, display_name, colors, row, col):
        """Создание карточки темы"""
        # Карточка
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            border_width=1,
            border_color="#e0e0e0",
            width=200,
            height=100,
            cursor="hand2"
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        card.grid_propagate(False)
        
        # Привязываем событие клика
        card.bind("<Button-1>", lambda e, n=theme_name: self.apply_theme(n))
        
        # Цветовая полоска сверху
        color_strip = ctk.CTkFrame(
            card,
            height=10,
            fg_color=colors[0],
            corner_radius=0
        )
        color_strip.pack(fill="x", side="top")
        color_strip.bind("<Button-1>", lambda e, n=theme_name: self.apply_theme(n))
        
        # Основное содержимое
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=10, pady=5)
        content_frame.bind("<Button-1>", lambda e, n=theme_name: self.apply_theme(n))
        
        # Название темы
        name_label = ctk.CTkLabel(
            content_frame,
            text=display_name,
            font=("Segoe UI", 14, "bold")
        )
        name_label.pack(anchor="w")
        name_label.bind("<Button-1>", lambda e, n=theme_name: self.apply_theme(n))
        
        # Превью цветов (маленькие квадратики)
        colors_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        colors_frame.pack(anchor="w", pady=5)
        colors_frame.bind("<Button-1>", lambda e, n=theme_name: self.apply_theme(n))
        
        for color in colors[:3]:  # Первые 3 цвета
            color_dot = ctk.CTkFrame(
                colors_frame,
                width=15,
                height=15,
                fg_color=color,
                corner_radius=3
            )
            color_dot.pack(side="left", padx=2)
            color_dot.bind("<Button-1>", lambda e, n=theme_name: self.apply_theme(n))
        
        # Кнопка выбора (маленькая)
        select_btn = ctk.CTkButton(
            content_frame,
            text="Выбрать",
            command=lambda n=theme_name: self.apply_theme(n),
            width=70,
            height=25,
            font=("Segoe UI", 11)
        )
        select_btn.pack(anchor="e", pady=2)
    
    def apply_theme(self, theme_name: str):
        """Применить тему"""
        if theme_manager.apply_theme(theme_name):
            display_names = {
                "emerald": "Изумрудная",
                "sapphire": "Сапфировая",
                "ruby": "Рубиновая",
                "amethyst": "Аметистовая",
                "midnight": "Полуночная",
                "sunrise": "Рассветная"
            }
            display_name = display_names.get(theme_name, theme_name.capitalize())
            self.notifier.show_success(f"✅ Тема '{display_name}' применена")
            self.dialog.after(300, self.destroy)