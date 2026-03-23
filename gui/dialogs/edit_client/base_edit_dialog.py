# -*- coding: utf-8 -*-

"""Базовый диалог редактирования клиента"""
import customtkinter as ctk

from gui.dialogs.base_dialog import BaseDialog
from gui.dialogs.styles import DialogStyles

from gui.dialogs.edit_client.form_widget import EditFormWidget
from gui.dialogs.edit_client.matrix_widget import EditMatrixWidget
from gui.dialogs.edit_client.date_widget import EditDateWidget
from gui.dialogs.edit_client.actions import EditActions
from gui.dialogs.edit_client.debug_paste import DebugPasteManager


class EditClientDialog(BaseDialog):
    """Диалог редактирования клиента"""
    
    def __init__(self, parent, db, client_id: int, callback, notifier):
        """
        Инициализация диалога редактирования
        
        Args:
            parent: родительское окно
            db: объект базы данных
            client_id: ID клиента
            callback: функция обратного вызова после сохранения
            notifier: объект для уведомлений
        """
        self.db = db
        self.client_id = client_id
        self.callback = callback
        self.notifier = notifier
        
        # Получение данных клиента
        self.client = db.get_client_by_id(client_id)
        if not self.client:
            notifier.show_error("❌ Клиент не найден")
            return
        
        self.matrices = db.get_all_matrices()
        
        # КВАДРАТНЫЙ РАЗМЕР: 500x500 с закругленными углами
        super().__init__(parent, f"✏️ Редактирование: {self.client.name}", 500, 500)
        
        # Настройка закругленных углов для диалога
        self.dialog.configure(corner_radius=15)
        
        # Инициализация компонентов
        self.form_widget = EditFormWidget(self)
        self.matrix_widget = EditMatrixWidget(self)
        self.date_widget = EditDateWidget(self)
        self.actions = EditActions(self)
        
        # Инициализация менеджера вставки
        self.paste_manager = DebugPasteManager(self.dialog, notifier, debug=True)
        
        self.create_content()
        self.bind_shortcuts()
        self.matrix_widget.load_matrices()
        
        # Привязываем вставку после создания всех полей
        self.after_id = self.dialog.after(100, self.bind_paste_to_all)
        self.dialog.after(200, self.force_paste_binding)
        
        # Тестируем буфер обмена
        self.paste_manager.test_clipboard()
        
        print(f"✅ EditClientDialog создан для клиента ID {client_id}")
    
    def create_content(self):
        """Создание содержимого"""
        # Заголовок с закругленными углами
        title_frame = ctk.CTkFrame(
            self.dialog, 
            fg_color=DialogStyles.COLOR_PRIMARY,
            corner_radius=10,
            height=40
        )
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="✏️ РЕДАКТИРОВАНИЕ КЛИЕНТА",
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )
        title_label.pack(expand=True)
        
        # Подсказка
        hint_label = ctk.CTkLabel(
            self.dialog,
            text="💡 Ctrl+Enter - сохранить | Esc - отмена | Ctrl+V - вставить",
            font=DialogStyles.FONT_HINT,
            text_color="gray"
        )
        hint_label.pack(pady=(0, 5))
        
        # Форма с закругленными углами
        form_container = ctk.CTkFrame(
            self.dialog, 
            fg_color="transparent",
            corner_radius=10
        )
        form_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Форма
        form_frame = self.form_widget.create_form(form_container)
        
        # Добавляем даты
        self.date_widget.create_birth_date_field(form_frame, self.form_widget.birth_row)
        self.date_widget.create_order_date_field(form_frame, self.form_widget.order_row)
        
        # Добавляем матрицу и цену
        self.matrix_widget.create_matrix_field(form_frame, self.form_widget.matrix_row, self.form_widget.price_row)
        
        # Кнопки внизу с закругленными углами
        self.actions.create_buttons()
    
    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.dialog.bind('<Control-Return>', lambda e: self.actions.save_client())
        self.dialog.bind('<Escape>', lambda e: self.destroy())
    
    def bind_paste_to_all(self):
        """Привязка Ctrl+V ко всем полям ввода"""
        self.paste_manager.log("\n🔧 НАЧАЛО ПРИВЯЗКИ ВСТАВКИ")
        
        # Собираем все поля ввода
        entries = {}
        
        # Поля из form_widget
        for name, widget in self.form_widget.get_all_widgets().items():
            entries[name] = widget
            self.paste_manager.log(f"📌 Найдено поле: {name}")
        
        # Поля из date_widget
        if self.date_widget.birth_entry:
            entries['birth_date'] = self.date_widget.birth_entry
            self.paste_manager.log("📌 Найдено поле: birth_date")
        if self.date_widget.order_date_entry:
            entries['order_date'] = self.date_widget.order_date_entry
            self.paste_manager.log("📌 Найдено поле: order_date")
        
        # Поля из matrix_widget
        if self.matrix_widget.price_entry:
            entries['price'] = self.matrix_widget.price_entry
            self.paste_manager.log("📌 Найдено поле: price")
        
        self.paste_manager.log(f"📋 Всего полей: {len(entries)}")
        
        # Привязываем вставку
        self.paste_manager.bind_paste_to_entries(entries)
        self.paste_manager.log("✅ Привязка завершена")
    
    def force_paste_binding(self):
        """Принудительная привязка вставки ко всем полям"""
        self.paste_manager.log("\n🔧 ПРИНУДИТЕЛЬНАЯ ПРИВЯЗКА")
        
        # Собираем все поля еще раз
        entries = {}
        
        # Поля из form_widget
        for name, widget in self.form_widget.get_all_widgets().items():
            entries[name] = widget
        
        # Поля из date_widget
        if self.date_widget.birth_entry:
            entries['birth_date'] = self.date_widget.birth_entry
        if self.date_widget.order_date_entry:
            entries['order_date'] = self.date_widget.order_date_entry
        
        # Поля из matrix_widget
        if self.matrix_widget.price_entry:
            entries['price'] = self.matrix_widget.price_entry
        
        # Привязываем заново
        self.paste_manager.bind_paste_to_entries(entries)
        
        # Также привязываем к самому диалогу
        def on_dialog_paste(event):
            self.paste_manager.log("📋 Событие вставки на уровне диалога")
            return "break"
        
        self.dialog.bind('<Control-v>', on_dialog_paste)
        self.dialog.bind('<Control-V>', on_dialog_paste)
        
        self.paste_manager.log("✅ Принудительная привязка завершена")