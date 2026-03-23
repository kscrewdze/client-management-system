# -*- coding: utf-8 -*-

"""Виджет для выбора матрицы и цены"""
import customtkinter as ctk
from gui.dialogs import CustomMatrixDialog


class MatrixWidget:
    """Класс для работы с матрицами и ценой"""
    
    def __init__(self, parent, notifier):
        self.parent = parent
        self.notifier = notifier
        self.matrices = []
        self.matrix_dict = {}
        self.matrix_var = None
        self.matrix_combo = None
        self.price_entry = None
    
    def create_matrix_field(self, parent_frame, row):
        """Создание поля для выбора матрицы и цены"""
        ctk.CTkLabel(
            parent_frame,
            text="📊 Матрица:*",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)
        
        matrix_price_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        matrix_price_frame.grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.matrix_var = ctk.StringVar()
        self.matrix_combo = ctk.CTkComboBox(
            matrix_price_frame,
            variable=self.matrix_var,
            values=[""],
            width=180,
            height=30,
            font=("Segoe UI", 11),
            state="readonly",
            command=self.on_matrix_selected
        )
        self.matrix_combo.pack(side="left")
        self.matrix_combo.bind('<<ComboboxSelected>>', self.on_matrix_selected)
        
        ctk.CTkLabel(
            matrix_price_frame,
            text="  Цена:",
            font=("Segoe UI", 11),
            text_color="gray"
        ).pack(side="left", padx=(5, 2))
        
        self.price_entry = ctk.CTkEntry(
            matrix_price_frame,
            width=100,
            height=30,
            font=("Segoe UI", 11),
            placeholder_text="0"
        )
        self.price_entry.pack(side="left")
        
        ctk.CTkLabel(
            matrix_price_frame,
            text="руб",
            font=("Segoe UI", 10),
            text_color="gray"
        ).pack(side="left", padx=(2, 0))
        
        return self.matrix_combo, self.price_entry
    
    def load_matrices(self, db):
        """Загрузка списка матриц из БД"""
        try:
            self.matrices = db.get_all_matrices()
            matrix_options = [""]
            matrix_options.append("✨ Свой выбор (указать цену)")
            
            self.matrix_dict = {}
            
            for m in self.matrices:
                option = f"{m.name} ({m.price:,.0f} руб.)"
                matrix_options.append(option)
                self.matrix_dict[option] = m
                print(f"✅ Загружена матрица: {option}")
            
            self.matrix_combo.configure(values=matrix_options)
            print(f"✅ Всего загружено матриц: {len(self.matrices)}")
            
        except Exception as e:
            print(f"❌ Ошибка загрузки матриц: {e}")
    
    def on_matrix_selected(self, event=None):
        """Обработка выбора матрицы"""
        selected = self.matrix_var.get()
        
        if not selected:
            return
        
        print(f"👉 Выбрана матрица: '{selected}'")
        
        if selected in self.matrix_dict:
            matrix = self.matrix_dict[selected]
            print(f"✅ Найдена матрица: {matrix.name}, цена: {matrix.price}")
            
            self.price_entry.delete(0, "end")
            if matrix.price.is_integer():
                price_str = str(int(matrix.price))
            else:
                price_str = str(matrix.price)
            self.price_entry.insert(0, price_str)
            self.notifier.show_success(f"💰 Цена: {price_str} руб.")
            
        elif selected == "✨ Свой выбор (указать цену)":
            dialog = CustomMatrixDialog(self.parent.winfo_toplevel(), self.notifier)
            self.parent.wait_window(dialog.dialog)
            
            if hasattr(dialog, 'result') and dialog.result:
                name, price = dialog.result
                self.matrix_var.set(name)
                self.price_entry.delete(0, "end")
                price_str = str(int(price)) if price.is_integer() else str(price)
                self.price_entry.insert(0, price_str)
                self.notifier.show_success(f"💰 Цена: {price_str} руб.")
    
    def get_matrix_info(self):
        """Получить информацию о выбранной матрице"""
        selected = self.matrix_var.get()
        matrix_name = selected
        matrix_id = None
        
        if selected in self.matrix_dict:
            matrix = self.matrix_dict[selected]
            matrix_name = matrix.name
            matrix_id = matrix.id
        
        return matrix_name, matrix_id
    
    def get_price(self):
        """Получить цену"""
        return self.price_entry.get().strip()
    
    def clear(self):
        """Очистить поля"""
        self.matrix_var.set("")
        self.price_entry.delete(0, "end")