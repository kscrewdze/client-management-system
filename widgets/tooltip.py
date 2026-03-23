# -*- coding: utf-8 -*-

"""Всплывающие подсказки"""
import tkinter as tk
from typing import Optional
import customtkinter as ctk


class ToolTip:
    """Класс для создания всплывающих подсказок"""
    
    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window: Optional[tk.Toplevel] = None
        self.after_id: Optional[str] = None
        
        widget.bind('<Enter>', self.schedule_tip)
        widget.bind('<Leave>', self.hide_tip)
        widget.bind('<Button>', self.hide_tip)
        widget.bind('<Motion>', self.on_motion)
    
    def schedule_tip(self, event=None):
        """Запланировать показ подсказки"""
        self.unschedule()
        if self.widget.winfo_exists():
            self.after_id = self.widget.after(self.delay, self.show_tip)
    
    def unschedule(self):
        """Отменить запланированный показ"""
        if self.after_id:
            try:
                if self.widget.winfo_exists():
                    self.widget.after_cancel(self.after_id)
            except Exception:
                pass
            finally:
                self.after_id = None
    
    def on_motion(self, event=None):
        """Скрыть подсказку при движении мыши"""
        self.hide_tip()
    
    def show_tip(self, event=None):
        """Показать подсказку"""
        if self.tip_window or not self.widget.winfo_exists():
            return
        
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                tw,
                text=self.text,
                justify=tk.LEFT,
                background="#ffffe0",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Segoe UI", 9),
                padx=8,
                pady=4
            )
            label.pack()
        except Exception:
            pass
    
    def hide_tip(self, event=None):
        """Скрыть подсказку"""
        self.unschedule()
        if self.tip_window:
            try:
                self.tip_window.destroy()
            except Exception:
                pass
            finally:
                self.tip_window = None