# -*- coding: utf-8 -*-

"""Базовый класс для всех диалоговых окон"""
import tkinter as tk
import customtkinter as ctk
from gui.dialogs.styles import DialogStyles


class BaseDialog:
    """Базовый класс для диалогов"""
    
    def __init__(self, parent, title="Диалог", width=None, height=None):
        """
        Инициализация базового диалога
        
        Args:
            parent: родительское окно
            title: заголовок диалога
            width: ширина окна
            height: высота окна
        """
        self.parent = parent
        self.result = None
        self.dialog = None
        self.width = width or DialogStyles.WIDTH_MEDIUM
        self.height = height or DialogStyles.HEIGHT_MEDIUM
        
        self.create_dialog(title)
        self.center_window()
    
    def create_dialog(self, title):
        """Создание окна диалога"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{self.width}x{self.height}")
        self.dialog.resizable(False, False)
        
        # Делаем модальным
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.focus_set()
    
    def center_window(self):
        """Центрирование окна"""
        self.dialog.update_idletasks()
        
        # Получаем размеры родительского окна
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Вычисляем позицию
        x = parent_x + (parent_width // 2) - (self.width // 2)
        y = parent_y + (parent_height // 2) - (self.height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def create_title(self, text, color=None):
        """Создание заголовка"""
        title_label = ctk.CTkLabel(
            self.dialog,
            text=text,
            font=DialogStyles.FONT_TITLE,
            text_color=color or DialogStyles.COLOR_PRIMARY
        )
        title_label.pack(pady=(DialogStyles.PADY, 5))
        return title_label
    
    def create_hint(self, text):
        """Создание подсказки"""
        hint_label = ctk.CTkLabel(
            self.dialog,
            text=text,
            font=DialogStyles.FONT_HINT,
            text_color="gray"
        )
        hint_label.pack()
        return hint_label
    
    def create_button(self, text, command, color=None, width=100):
        """Создание кнопки"""
        btn = ctk.CTkButton(
            self.dialog,
            text=text,
            command=command,
            width=width,
            height=32,
            font=DialogStyles.FONT_NORMAL,
            fg_color=color or DialogStyles.COLOR_GRAY,
            hover_color=self._darken_color(color or DialogStyles.COLOR_GRAY)
        )
        return btn
    
    def _darken_color(self, color):
        """Затемнение цвета для hover эффекта"""
        darken_map = {
            DialogStyles.COLOR_PRIMARY: "#1e3f5c",
            DialogStyles.COLOR_SUCCESS: "#1e5a23",
            DialogStyles.COLOR_WARNING: "#db6a00",
            DialogStyles.COLOR_ERROR: "#b71c1c",
            DialogStyles.COLOR_INFO: "#0277bd",
            DialogStyles.COLOR_GRAY: "#616161"
        }
        return darken_map.get(color, color)
    
    def bind_paste_shortcut(self, entry):
        """Привязка Ctrl+V к полю ввода"""
        def on_paste(event):
            try:
                clipboard = self.dialog.clipboard_get()
                if clipboard:
                    entry.insert("insert", clipboard)
                return "break"
            except:
                return "break"
        
        entry.bind('<Control-v>', on_paste)
        entry.bind('<Control-V>', on_paste)
        entry.bind('<Command-v>', on_paste)
        entry.bind('<Command-V>', on_paste)
        entry.bind('<Shift-Insert>', on_paste)
    
    def destroy(self):
        """Закрытие диалога"""
        if self.dialog:
            self.dialog.destroy()