# -*- coding: utf-8 -*-

"""Диалог для создания своей матрицы"""
import customtkinter as ctk
from gui.dialogs.base_dialog import BaseDialog
from gui.dialogs.styles import DialogStyles


class CustomMatrixDialog(BaseDialog):
    """Диалог для создания своей матрицы"""
    
    def __init__(self, parent, notifier):
        """
        Инициализация диалога
        
        Args:
            parent: родительское окно
            notifier: объект для уведомлений
        """
        self.notifier = notifier
        super().__init__(parent, "✨ Свой выбор", 350, 220)
        self.create_content()
        self.bind_shortcuts()
        print("✅ CustomMatrixDialog создан")
    
    def create_content(self):
        """Создание содержимого диалога"""
        # Заголовок
        self.create_title("✨ СВОЙ ВЫБОР", DialogStyles.COLOR_PRIMARY)
        
        # Форма
        form_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        form_frame.pack(pady=5, padx=DialogStyles.PADX, fill="x")
        
        # Название
        ctk.CTkLabel(
            form_frame,
            text="Название:",
            font=DialogStyles.FONT_NORMAL,
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        self.name_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=30,
            font=DialogStyles.FONT_NORMAL,
            placeholder_text="Например: Индивидуальный разбор"
        )
        self.name_entry.pack(pady=(0, 5))
        self.name_entry.insert(0, "Свой выбор")
        
        # Привязываем Ctrl+V
        self.bind_paste_shortcut(self.name_entry)
        
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
        
        # Подсказка
        hint_label = ctk.CTkLabel(
            form_frame,
            text="💡 Можно ввести 0 для бесплатно",
            font=DialogStyles.FONT_HINT,
            text_color="gray"
        )
        hint_label.pack(anchor="w")
        
        # Кнопки
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        save_btn = self.create_button(
            "✅ Применить",
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
        
        # Фокус на поле цены
        self.price_entry.focus()
    
    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.destroy())
    
    def save(self):
        """Сохранение своей матрицы"""
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        if not name:
            self.notifier.show_error("❌ Введите название!")
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