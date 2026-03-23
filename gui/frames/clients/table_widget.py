# -*- coding: utf-8 -*-

"""Виджет таблицы клиентов"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import logging

logger = logging.getLogger(__name__)


class TableWidget:
    """Класс для работы с таблицей клиентов"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.notifier = parent.notifier
        self.tree = None
        self.selected_item = None
        self.tooltip = None
        self.rows_frame = None
        self.canvas = None
        self.scrollbar = None
    
    def create_table(self):
        """Создание таблицы"""
        table_container = ctk.CTkFrame(self.parent)
        table_container.pack(fill="both", expand=True, pady=(0, 5))
        
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        
        columns = ("status", "name", "telegram", "phone", "birth", "destiny", "matrix", "price", "order_date")
        
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=20
        )
        
        # Настройка колонок
        self.tree.heading("status", text="✅")
        self.tree.column("status", width=50, anchor="center")
        
        self.tree.heading("name", text="Имя")
        self.tree.column("name", width=200, anchor="w")
        
        self.tree.heading("telegram", text="Telegram")
        self.tree.column("telegram", width=150, anchor="w")
        
        self.tree.heading("phone", text="Телефон")
        self.tree.column("phone", width=150, anchor="w")
        
        self.tree.heading("birth", text="Дата рожд.")
        self.tree.column("birth", width=100, anchor="center")
        
        self.tree.heading("destiny", text="Число")
        self.tree.column("destiny", width=60, anchor="center")
        
        self.tree.heading("matrix", text="Матрица")
        self.tree.column("matrix", width=200, anchor="w")
        
        self.tree.heading("price", text="Цена")
        self.tree.column("price", width=100, anchor="e")
        
        self.tree.heading("order_date", text="Дата заказа")
        self.tree.column("order_date", width=100, anchor="center")
        
        # Скроллбары
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # События
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.tree.bind("<Double-Button-1>", self.on_tree_double_click)
        self.tree.bind("<Motion>", self.on_tree_motion)
        self.tree.bind("<Leave>", self.hide_comment_tooltip)
    
    def refresh(self, clients=None):
        """Обновление списка клиентов"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if clients is None:
                clients = self.db.get_all_clients()
            
            if not clients:
                self.parent.status_label.configure(text="📭 Нет данных")
                return
            
            for client in clients:
                price = f"{client.service_price:,.0f} ₽".replace(",", " ")
                status = "✅" if client.is_completed else "⬜"
                
                name = client.name
                if len(name) > 25:
                    name = name[:22] + "..."
                
                telegram_original = client.telegram or "—"
                telegram_display = telegram_original
                if telegram_display != "—" and len(telegram_display) > 20:
                    telegram_display = telegram_display[:17] + "..."
                
                phone = client.phone or "—"
                if phone != "—" and len(phone) > 15:
                    phone = phone[:12] + "..."
                
                matrix = client.matrix_name or "—"
                if matrix != "—" and len(matrix) > 25:
                    matrix = matrix[:22] + "..."
                
                values = [
                    status,
                    name,
                    telegram_display,
                    phone,
                    client.birth_date,
                    str(client.destiny_number),
                    matrix,
                    price,
                    client.order_date
                ]
                
                comment = client.comment or "—"
                item_id = self.tree.insert("", "end", values=values, 
                                          tags=(comment, telegram_original))
                
                if client.is_completed:
                    self.tree.tag_configure("completed", background="#e8f5e8")
                    self.tree.item(item_id, tags=(comment, telegram_original, "completed"))
            
            self.parent.status_label.configure(text=f"📊 Всего: {len(clients)}")
            
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            self.notifier.show_error(f"❌ Ошибка загрузки: {str(e)}")
    
    def on_tree_select(self, event):
        """Выбор элемента в дереве"""
        self.selected_item = self.tree.selection()
        self.parent.selected_item = self.selected_item
    
    def on_tree_double_click(self, event):
        """Двойной клик - копирование Telegram"""
        try:
            region = self.tree.identify_region(event.x, event.y)
            if region == "cell":
                item = self.tree.identify_row(event.y)
                if item:
                    self.selected_item = (item,)
                    self.parent.selected_item = self.selected_item
                    self.parent.copy_telegram()
        except Exception as e:
            logger.error(f"Ошибка при двойном клике: {e}")
    
    def on_tree_motion(self, event):
        """Подсказка при наведении"""
        try:
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            if item and column == "#2":  # Колонка имени
                tags = self.tree.item(item, "tags")
                if tags and len(tags) > 0:
                    comment = tags[0]
                    if comment and comment != "—":
                        self.show_comment_tooltip(event, comment)
            else:
                self.hide_comment_tooltip()
        except:
            pass
    
    def show_comment_tooltip(self, event, comment):
        """Показать подсказку с комментарием"""
        self.hide_comment_tooltip()
        
        self.tooltip = tk.Toplevel(self.parent)
        self.tooltip.wm_overrideredirect(True)
        
        x = event.x_root + 15
        y = event.y_root + 10
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        frame = tk.Frame(self.tooltip, bg="#ffffe0", relief="solid", borderwidth=1)
        frame.pack()
        
        label = tk.Label(
            frame,
            text=f"💬 {comment}",
            bg="#ffffe0",
            padx=15,
            pady=8,
            font=("Segoe UI", 11),
            wraplength=300,
            justify="left"
        )
        label.pack()
    
    def hide_comment_tooltip(self, event=None):
        """Скрыть подсказку"""
        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def get_selected_client_telegram(self):
        """Получить Telegram выбранного клиента"""
        if not self.selected_item:
            return None
        
        item = self.selected_item[0]
        tags = self.tree.item(item, "tags")
        
        if tags and len(tags) >= 2:
            telegram = tags[1]
            if telegram and telegram != "—":
                return telegram
        
        return None
    
    def get_selected_client_id(self):
        """Получить ID выбранного клиента"""
        if not self.selected_item:
            return None
        
        item = self.selected_item[0]
        values = self.tree.item(item, "values")
        
        if not values or len(values) < 2:
            return None
        
        client_name = values[1].replace("...", "")
        
        clients = self.db.get_all_clients()
        for client in clients:
            if client.name.startswith(client_name) or client_name in client.name:
                return client.id
        
        return None