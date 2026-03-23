# -*- coding: utf-8 -*-

"""Карточка для экспорта в Excel"""
from gui.frames.export.cards.base_card import BaseExportCard


class ExcelCard(BaseExportCard):
    """Карточка экспорта в Excel"""
    
    def __init__(self, parent, command, column):
        super().__init__(
            parent=parent,
            title="Excel",
            subtitle="Экспорт в Microsoft Excel",
            description="Экспортировать всех клиентов\nв формате Excel (.xlsx)",
            color="#217346",
            emoji="📗",
            command=command,
            column=column
        )