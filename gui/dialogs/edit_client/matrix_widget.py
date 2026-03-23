# -*- coding: utf-8 -*-

"""Виджет для выбора матрицы в редактировании"""
import customtkinter as ctk
from gui.dialogs.styles import DialogStyles
from gui.dialogs.custom_matrix_dialog import CustomMatrixDialog


class EditMatrixWidget:
    """Класс для работы с матрицами в редактировании"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = parent.dialog
        self.client = parent.client
        self.matrices = parent.matrices
        self.notifier = parent.notifier
        self.matrix_dict = {}
        self.matrix_var = None
        self.matrix_combo = None
        self.price_entry = None
    
    def load_matrices(self):
        """Загрузка списка матриц"""
        matrix_options = [""]
        matrix_options.append("✨ Свой выбор (указать цену)")
        self.matrix_dict = {}
        
        for m in self.matrices:
            option = f"{m.name} ({m.price:,.0f} руб.)"
            matrix_options.append(option)
            self.matrix_dict[option] = m
        
        self.matrix_combo.configure(values=matrix_options)
        
        # Установка текущего значения
        if self.client.matrix_id:
            for m in self.matrices:
                if m.id == self.client.matrix_id:
                    self.matrix_var.set(f"{m.name} ({m.price:,.0f} руб.)")
                    break
    
    def create_matrix_field(self, form_frame, matrix_row, price_row):
        """Создание полей для матрицы и цены"""
        # Матрица
        ctk.CTkLabel(
            form_frame,
            text="📊 Матрица:",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=matrix_row, column=0, sticky="w", pady=2)
        
        matrix_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        matrix_frame.grid(row=matrix_row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.matrix_var = ctk.StringVar()
        self.matrix_combo = ctk.CTkComboBox(
            matrix_frame,
            variable=self.matrix_var,
            values=[""],
            width=200,
            height=30,
            font=DialogStyles.FONT_NORMAL,
            state="readonly"
        )
        self.matrix_combo.pack(side="left")
        self.matrix_combo.bind('<<ComboboxSelected>>', self.on_matrix_selected)
        
        # Цена
        ctk.CTkLabel(
            form_frame,
            text="💰 Цена:*",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).grid(row=price_row, column=0, sticky="w", pady=2)
        
        price_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        price_frame.grid(row=price_row, column=1, sticky="w", pady=2, padx=(5, 0))
        
        self.price_entry = ctk.CTkEntry(
            price_frame,
            width=100,
            height=30,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="0"
        )
        self.price_entry.pack(side="left")
        
        # Устанавливаем цену клиента
        price_value = str(int(self.client.service_price)) if self.client.service_price.is_integer() else str(self.client.service_price)
        self.price_entry.insert(0, price_value)
        self.parent.bind_paste_shortcut(self.price_entry)
        
        ctk.CTkLabel(
            price_frame,
            text="руб",
            font=DialogStyles.FONT_SMALL,
            text_color="gray"
        ).pack(side="left", padx=(2, 0))
    
    def on_matrix_selected(self, event=None):
        """Обработка выбора матрицы"""
        selected = self.matrix_var.get()
        
        if not selected:
            return
        
        if selected == "✨ Свой выбор (указать цену)":
            dialog = CustomMatrixDialog(self.dialog, self.notifier)
            self.dialog.wait_window(dialog.dialog)
            
            if hasattr(dialog, 'result') and dialog.result:
                name, price = dialog.result
                self.matrix_var.set(name)
                self.price_entry.delete(0, "end")
                price_str = str(int(price)) if price.is_integer() else str(price)
                self.price_entry.insert(0, price_str)
            
            self.matrix_var.set("")
        
        elif selected in self.matrix_dict:
            matrix = self.matrix_dict[selected]
            self.price_entry.delete(0, "end")
            price_str = str(int(matrix.price)) if matrix.price.is_integer() else str(matrix.price)
            self.price_entry.insert(0, price_str)
    
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