# -*- coding: utf-8 -*-

"""Действия для работы с матрицами"""
from tkinter import messagebox
import customtkinter as ctk
from widgets.tooltip import ToolTip
from gui.dialogs import MatrixDialog
from gui.frames.matrices.styles import MatrixStyles


class MatrixActions:
    """Класс для действий с матрицами"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.notifier = parent.notifier
        self.refresh_callback = parent.refresh_callback
    
    def create_toolbar(self, parent_frame):
        """Создание панели инструментов"""
        toolbar = ctk.CTkFrame(parent_frame, fg_color="transparent", height=50)
        toolbar.pack(fill="x", pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # Заголовок слева
        title = ctk.CTkLabel(
            toolbar,
            text="📊 УПРАВЛЕНИЕ МАТРИЦАМИ",
            font=MatrixStyles.TITLE_FONT,
            text_color=MatrixStyles.PRIMARY
        )
        title.pack(side="left", padx=5)
        
        # Кнопки справа
        buttons_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Кнопка добавления
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Добавить",
            command=self.add_matrix,
            width=120,
            height=MatrixStyles.BUTTON_HEIGHT,
            font=MatrixStyles.NORMAL_FONT,
            fg_color=MatrixStyles.SUCCESS,
            hover_color="#1e5a23"
        )
        add_btn.pack(side="left", padx=2)
        ToolTip(add_btn, "Добавить новую матрицу")
        
        # Кнопка редактирования
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Редактировать",
            command=self.edit_selected,
            width=130,
            height=MatrixStyles.BUTTON_HEIGHT,
            font=MatrixStyles.NORMAL_FONT,
            fg_color=MatrixStyles.WARNING,
            hover_color="#db6a00"
        )
        edit_btn.pack(side="left", padx=2)
        ToolTip(edit_btn, "Редактировать выбранную матрицу")
        
        # Кнопка удаления
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑 Удалить",
            command=self.delete_selected,
            width=100,
            height=MatrixStyles.BUTTON_HEIGHT,
            font=MatrixStyles.NORMAL_FONT,
            fg_color=MatrixStyles.ERROR,
            hover_color="#b71c1c"
        )
        delete_btn.pack(side="left", padx=2)
        ToolTip(delete_btn, "Удалить выбранную матрицу")
        
        return toolbar
    
    def add_matrix(self):
        """Добавление матрицы"""
        dialog = MatrixDialog(self.parent.winfo_toplevel(), self.notifier)
        self.parent.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result') and dialog.result:
            name, price = dialog.result
            matrix_id = self.db.add_matrix(name, price)
            if matrix_id:
                self.notifier.show_success(f"✅ Матрица '{name}' добавлена")
                self.refresh_callback()
            else:
                self.notifier.show_error("❌ Матрица с таким названием уже существует")
    
    def edit_selected(self):
        """Редактирование выбранной матрицы"""
        matrix_id = self.parent.table_widget.get_selected_matrix_id()
        if not matrix_id:
            self.notifier.show_warning("⚠️ Выберите матрицу")
            return
        
        matrix = self.db.get_matrix_by_id(matrix_id)
        if not matrix:
            return
        
        dialog = MatrixDialog(
            self.parent.winfo_toplevel(),
            self.notifier,
            matrix_id,
            (matrix.id, matrix.name, matrix.price, matrix.created_date)
        )
        self.parent.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result') and dialog.result:
            name, price = dialog.result
            self.db.update_matrix(matrix_id, name, price)
            self.notifier.show_success(f"✅ Матрица обновлена")
            self.refresh_callback()
    
    def delete_selected(self):
        """Удаление выбранной матрицы"""
        matrix_id = self.parent.table_widget.get_selected_matrix_id()
        if not matrix_id:
            self.notifier.show_warning("⚠️ Выберите матрицу")
            return
        
        matrix_name = self.parent.table_widget.get_selected_matrix_name()
        
        if messagebox.askyesno(
            "Подтверждение",
            f"Удалить матрицу '{matrix_name}'?\nВсе связанные клиенты будут отвязаны."
        ):
            self.db.delete_matrix(matrix_id)
            self.refresh_callback()
            self.notifier.show_success(f"✅ Матрица удалена")