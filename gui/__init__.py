# Пакет GUI
from gui.main import MainApplication

# Экспортируем основные классы для обратной совместимости
from gui.frames.statistics_frame import StatisticsFrame
from gui.frames.clients import ClientsListFrame
from gui.frames.matrices import MatricesFrame  # ИСПРАВЛЕНО: было matrices_frame
from gui.frames.add_client import AddClientFrame
from gui.frames.export import ExportFrame
from gui.frames.settings import ThemesFrame

__all__ = [
    'MainApplication',
    'StatisticsFrame',
    'ClientsListFrame',
    'MatricesFrame',
    'AddClientFrame',
    'ExportFrame',
    'ThemesFrame'
]