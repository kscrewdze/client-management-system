# -*- coding: utf-8 -*-

"""Горячие клавиши для фрейма клиентов"""


class Shortcuts:
    """Класс для управления горячими клавишами"""
    
    def __init__(self, parent):
        self.parent = parent
    
    def bind_shortcuts(self):
        """Привязать горячие клавиши"""
        root = self.parent.winfo_toplevel()
        root.bind('<Control-e>', lambda e: self.parent.edit_selected())
        root.bind('<Control-E>', lambda e: self.parent.edit_selected())
        root.bind('<Control-d>', lambda e: self.parent.delete_selected())
        root.bind('<Control-D>', lambda e: self.parent.delete_selected())
        root.bind('<Control-r>', lambda e: self.parent.refresh())
        root.bind('<Control-R>', lambda e: self.parent.refresh())
        root.bind('<Control-f>', lambda e: self.parent.search_entry.focus())
        root.bind('<Control-F>', lambda e: self.parent.search_entry.focus())