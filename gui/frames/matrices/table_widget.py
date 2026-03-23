# -*- coding: utf-8 -*-

"""Виджет таблицы матриц"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from gui.frames.matrices.styles import MatrixStyles


class MatrixTableWidget:
    """Класс для работы с таблицей матриц"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.notifier = parent.notifier
        self.tree = None
        self.selected_item = None
    
    def create_table(self, parent_frame):
        """Создание таблицы без колонки ID"""
        # Фрейм для таблицы
        table_frame = ctk.CTkFrame(parent_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Стиль для Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       font=MatrixStyles.NORMAL_FONT, 
                       rowheight=MatrixStyles.TABLE_ROW_HEIGHT)
        style.configure("Treeview.Heading", 
                       font=MatrixStyles.HEADER_FONT)
        
        # Колонки (ID исключен)
        columns = ("name", "price", "created_date")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Настраиваем заголовки
        self.tree.heading("name", text="Название матрицы")
        self.tree.heading("price", text="Цена")
        self.tree.heading("created_date", text="Дата создания")
        
        # Настраиваем ширину колонок
        self.tree.column("name", width=300, anchor="w")
        self.tree.column("price", width=150, anchor="center")
        self.tree.column("created_date", width=150, anchor="center")
        
        # Добавляем скроллбары
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Размещаем
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Привязываем события
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.tree.bind("<Double-Button-1>", lambda e: self.parent.edit_selected())
        
        return self.tree
    
    def refresh(self, matrices=None):
        """Обновление таблицы"""
        # Очищаем
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем данные
        if matrices is None:
            matrices = self.db.get_all_matrices()
        
        # Заполняем
        for matrix in matrices:
            # Форматируем дату
            created = matrix.created_date[:10] if matrix.created_date else "—"
            
            # Форматируем цену
            price = f"{matrix.price:,.0f} руб.".replace(",", " ")
            
            values = (
                matrix.name,
                price,
                created
            )
            
            # Сохраняем ID в скрытом виде
            item_id = self.tree.insert("", "end", values=values)
            self.tree.item(item_id, tags=(str(matrix.id),))
        
        return len(matrices)
    
    def on_select(self, event):
        """Обработка выбора строки"""
        selection = self.tree.selection()
        if selection:
            self.selected_item = selection[0]
    
    def get_selected_matrix_id(self):
        """Получить ID выбранной матрицы"""
        if not self.selected_item:
            return None
        
        tags = self.tree.item(self.selected_item, "tags")
        if tags:
            return int(tags[0])
        return None
    
    def get_selected_matrix_name(self):
        """Получить название выбранной матрицы"""
        if not self.selected_item:
            return None
        
        values = self.tree.item(self.selected_item, "values")
        if values:
            return values[0]
        return None