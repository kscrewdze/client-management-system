# -*- coding: utf-8 -*-

"""Карточка для экспорта в JSON"""
from gui.frames.export.cards.base_card import BaseExportCard


class JsonCard(BaseExportCard):
    """Карточка экспорта в JSON"""
    
    def __init__(self, parent, command, column):
        super().__init__(
            parent=parent,
            title="JSON",
            subtitle="Экспорт в JSON",
            description="Экспортировать всех клиентов\nв формате JSON",
            color="#f7df1e",
            emoji="📋",
            command=command,
            column=column
        )