# -*- coding: utf-8 -*-

"""Действия с клиентами"""
from tkinter import messagebox
import customtkinter as ctk
from widgets.tooltip import ToolTip

# ИСПРАВЛЕННЫЙ ИМПОРТ
from gui.dialogs import EditClientDialog


class ClientActions:
    """Класс для действий с клиентами"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.notifier = parent.notifier
        self.refresh_callback = parent.refresh_callback
    
    def create_buttons_frame(self):
        """Создание панели с кнопками действий"""
        buttons_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # Кнопка Обновить
        refresh_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Обновить",
            command=self.parent.refresh,
            width=100,
            height=36,
            font=("Segoe UI", 11, "bold"),
            fg_color="#0288d1",
            hover_color="#0277bd"
        )
        refresh_btn.pack(side="left", padx=3)
        ToolTip(refresh_btn, "Обновить список (Ctrl+R)")
        
        # Кнопка Редактировать
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Редактировать",
            command=self.edit_selected,
            width=120,
            height=36,
            font=("Segoe UI", 11, "bold"),
            fg_color="#ed6c02",
            hover_color="#db6a00"
        )
        edit_btn.pack(side="left", padx=3)
        ToolTip(edit_btn, "Редактировать выбранного клиента")
        
        # Кнопка Удалить
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑 Удалить",
            command=self.delete_selected,
            width=100,
            height=36,
            font=("Segoe UI", 11, "bold"),
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        delete_btn.pack(side="left", padx=3)
        ToolTip(delete_btn, "Удалить выбранного клиента")
        
        # Кнопка Отметить
        toggle_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Отметить",
            command=self.toggle_completed,
            width=110,
            height=36,
            font=("Segoe UI", 11, "bold"),
            fg_color="#2e7d32",
            hover_color="#1e5a23"
        )
        toggle_btn.pack(side="left", padx=3)
        ToolTip(toggle_btn, "Отметить как выполненный/невыполненный")
        
        return buttons_frame
    
    def copy_telegram(self):
        """Копировать Telegram в буфер обмена"""
        telegram = self.parent.get_selected_client_telegram()
        
        if not telegram or telegram == "—":
            self.notifier.show_warning("⚠️ У клиента нет Telegram")
            return
        
        self.parent.clipboard_clear()
        self.parent.clipboard_append(telegram)
        self.notifier.show_success(f"📋 {telegram} скопирован")
    
    def toggle_completed(self):
        """Переключить статус выполнения"""
        client_id = self.parent.get_selected_client_id()
        if not client_id:
            self.notifier.show_warning("⚠️ Выберите клиента")
            return
        
        self.db.toggle_completed(client_id)
        self.parent.refresh()
        self.refresh_callback()
    
    def edit_selected(self):
        """Редактировать выбранного клиента"""
        client_id = self.parent.get_selected_client_id()
        if not client_id:
            self.notifier.show_warning("⚠️ Выберите клиента")
            return
        
        # ИСПРАВЛЕННЫЙ ИМПОРТ - используем from gui.dialogs import EditClientDialog
        EditClientDialog(
            self.parent.winfo_toplevel(),
            self.db,
            client_id,
            self.refresh_callback,
            self.notifier
        )
    
    def delete_selected(self):
        """Удалить выбранного клиента"""
        client_id = self.parent.get_selected_client_id()
        if not client_id:
            self.notifier.show_warning("⚠️ Выберите клиента")
            return
        
        client = self.db.get_client_by_id(client_id)
        if not client:
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить клиента '{client.name}'?"):
            self.db.delete_client(client_id)
            self.parent.refresh()
            self.refresh_callback()