# Пакет фреймов
from gui.frames.statistics_frame import StatisticsFrame
from gui.frames.clients import ClientsListFrame
from gui.frames.matrices import MatricesFrame
from gui.frames.add_client import AddClientFrame  # ДОЛЖНО БЫТЬ add_client
from gui.frames.export import ExportFrame
from gui.frames.settings import ThemesFrame

__all__ = [
    'StatisticsFrame',
    'ClientsListFrame',
    'MatricesFrame',
    'AddClientFrame',
    'ExportFrame',
    'ThemesFrame'
]