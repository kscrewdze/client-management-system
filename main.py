#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главный модуль приложения
Автор: kScrewdze
Описание: Современное приложение для управления клиентами и матрицами
GUI: PySide6 (Qt6)
"""

import sys
import os
import warnings
import logging

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Инициализация логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    """Точка входа в приложение"""
    try:
        logger.info("=" * 50)
        logger.info("ЗАПУСК ПРИЛОЖЕНИЯ (PySide6)")
        logger.info("=" * 50)

        # Настройка frozen-окружения (.exe)
        from build_exe_hooks import setup_frozen_env
        setup_frozen_env()

        from gui_qt import run_app
        run_app()

    except Exception as e:
        logger.critical("Критическая ошибка при запуске: %s", e, exc_info=True)
        raise

    finally:
        logger.info("=" * 50)
        logger.info("ЗАВЕРШЕНИЕ РАБОТЫ")
        logger.info("=" * 50)


if __name__ == "__main__":
    main()