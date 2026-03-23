# -*- coding: utf-8 -*-

"""Виджет предпросмотра темы"""
import customtkinter as ctk


class PreviewWidget:
    """Виджет для предпросмотра цветов темы"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.frame = None
    
    def create(self):
        """Создать виджет предпросмотра"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        colors = [
            ("Основной", self.theme.colors.primary),
            ("Второстепенный", self.theme.colors.secondary),
            ("Фон", self.theme.colors.background),
            ("Текст", self.theme.colors.text_primary)
        ]
        
        for name, color in colors:
            self._create_color_row(name, color)
        
        return self.frame
    
    def _create_color_row(self, name, color):
        """Создать строку с цветом"""
        row = ctk.CTkFrame(self.frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        color_box = ctk.CTkFrame(
            row,
            width=20,
            height=20,
            fg_color=color,
            corner_radius=3
        )
        color_box.pack(side="left", padx=(0, 5))
        color_box.pack_propagate(False)
        
        color_label = ctk.CTkLabel(
            row,
            text=f"{name}: {color}",
            font=("Segoe UI", 10)
        )
        color_label.pack(side="left")
    
    def update_theme(self, theme):
        """Обновить тему"""
        self.theme = theme
        # Очищаем и создаем заново
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create()