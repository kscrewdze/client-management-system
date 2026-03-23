# -*- coding: utf-8 -*-

"""Ненавязчивые уведомления"""
import tkinter as tk
from typing import Optional
import customtkinter as ctk


class NotificationLabel:
    """Класс для создания ненавязчивых уведомлений"""
    
    def __init__(self, parent):
        self.parent = parent
        self.label: Optional[ctk.CTkLabel] = None
        self.after_id: Optional[str] = None
    
    def show(self, message: str, duration: int = 2000, color: str = "#2e7d32"):
        """Показать уведомление"""
        self.hide()
        
        try:
            self.label = ctk.CTkLabel(
                self.parent,
                text=message,
                fg_color=color,
                text_color="white",
                font=("Segoe UI", 12, "bold"),
                corner_radius=8,
                padx=20,
                pady=10
            )
            
            self.label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
            self.label.lift()
            
            if self.parent.winfo_exists():
                self.after_id = self.parent.after(duration, self.hide)
        except Exception:
            pass
    
    def show_error(self, message: str, duration: int = 3000):
        """Показать ошибку"""
        self.show(message, duration, "#d32f2f")
    
    def show_success(self, message: str, duration: int = 2000):
        """Показать успех"""
        self.show(message, duration, "#2e7d32")
    
    def show_info(self, message: str, duration: int = 2000):
        """Показать информацию"""
        self.show(message, duration, "#0288d1")
    
    def show_warning(self, message: str, duration: int = 2500):
        """Показать предупреждение"""
        self.show(message, duration, "#ed6c02")
    
    def hide(self):
        """Скрыть уведомление"""
        if self.after_id:
            try:
                if self.parent.winfo_exists():
                    self.parent.after_cancel(self.after_id)
            except Exception:
                pass
            finally:
                self.after_id = None
        
        if self.label:
            try:
                self.label.destroy()
            except Exception:
                pass
            finally:
                self.label = None