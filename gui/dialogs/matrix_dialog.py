# -*- coding: utf-8 -*-

"""Диалог для добавления/редактирования матрицы"""
import customtkinter as ctk
from gui.dialogs.base_dialog import BaseDialog
from gui.dialogs.styles import DialogStyles


class MatrixDialog(BaseDialog):
    """Диалог для добавления/редактирования матрицы"""
    
    def __init__(self, parent, notifier, matrix_id=None, matrix_data=None):
        """
        Инициализация диалога
        
        Args:
            parent: родительское окно
            notifier: объект для уведомлений
            matrix_id: ID матрицы (для редактирования)
            matrix_data: данные матрицы (для редактирования)
        """
        self.notifier = notifier
        self.matrix_id = matrix_id
        self.matrix_data = matrix_data
        
        title = "✏️ Редактирование матрицы" if matrix_id else "➕ Добавление матрицы"
        super().__init__(parent, title, 350, 200)
        self.create_content()
        self.bind_shortcuts()
        print(f"✅ MatrixDialog создан: {title}")
    
    def create_content(self):
        """Создание содержимого диалога"""
        # Заголовок
        title_text = "✏️ РЕДАКТИРОВАНИЕ" if self.matrix_id else "➕ ДОБАВЛЕНИЕ"
        self.create_title(title_text, DialogStyles.COLOR_PRIMARY)
        
        # Форма
        form_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        form_frame.pack(pady=5, padx=DialogStyles.PADX, fill="x")
        
        # Название
        ctk.CTkLabel(
            form_frame,
            text="Название матрицы:",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        self.name_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=30,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="Введите название"
        )
        self.name_entry.pack(pady=(0, 5))
        
        # Привязываем Ctrl+V
        self.bind_paste_shortcut(self.name_entry)
        
        if self.matrix_data:
            self.name_entry.insert(0, self.matrix_data[1])
        
        # Цена
        ctk.CTkLabel(
            form_frame,
            text="Цена (руб):",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        self.price_entry = ctk.CTkEntry(
            form_frame,
            width=200,
            height=30,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="0"
        )
        self.price_entry.pack(pady=(0, 2))
        
        # Привязываем Ctrl+V
        self.bind_paste_shortcut(self.price_entry)
        
        if self.matrix_data:
            self.price_entry.insert(0, str(self.matrix_data[2]))
        
        # Кнопки
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        save_btn = self.create_button(
            "💾 Сохранить",
            self.save,
            DialogStyles.COLOR_SUCCESS,
            120
        )
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = self.create_button(
            "❌ Отмена",
            self.destroy,
            DialogStyles.COLOR_ERROR,
            100
        )
        cancel_btn.pack(side="left", padx=5)
        
        # Фокус на поле названия
        self.name_entry.focus()
    
    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.destroy())
    
    def save(self):
        """Сохранение матрицы"""
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        if not name:
            self.notifier.show_error("❌ Введите название матрицы!")
            self.name_entry.focus()
            return
        
        if not price_str:
            self.notifier.show_error("❌ Введите цену!")
            self.price_entry.focus()
            return
        
        try:
            price = float(price_str.replace(',', '.'))
            if price < 0:
                self.notifier.show_error("❌ Цена не может быть отрицательной!")
                self.price_entry.focus()
                return
        except ValueError:
            self.notifier.show_error("❌ Цена должна быть числом!")
            self.price_entry.focus()
            return
        
        self.result = (name, price)
        self.destroy()