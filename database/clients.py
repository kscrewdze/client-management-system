
# -*- coding: utf-8 -*-

"""Работа с клиентами в БД"""
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from database.models import Client

logger = logging.getLogger(__name__)


class ClientsDB:
    """Класс для работы с клиентами."""

    def __init__(self, db) -> None:
        self.db = db

    def add_client(self, client_data: Dict[str, Any]) -> int:
        """Добавление нового клиента.

        Args:
            client_data: Словарь с данными клиента.

        Returns:
            ID добавленного клиента.

        Raises:
            sqlite3.Error: При ошибке записи в БД.
        """
        try:
            with self.db._lock:
                self.db.cursor.execute('''
                    INSERT INTO clients (
                        name, telegram, birth_date, destiny_number, matrix_id,
                        service_name, service_price, comment, phone, order_date, created_date,
                        is_completed, completed_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    client_data['name'],
                    client_data.get('telegram'),
                    client_data['birth_date'],
                    client_data['destiny_number'],
                    client_data.get('matrix_id'),
                    client_data['service_name'],
                    client_data['service_price'],
                    client_data.get('comment'),
                    client_data.get('phone'),
                    client_data['order_date'],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    0, None,
                ))
                self.db.conn.commit()
                client_id = self.db.cursor.lastrowid
            logger.info("Добавлен клиент: %s (ID: %d)", client_data['name'], client_id)
            return client_id
        except Exception as e:
            logger.error("Ошибка добавления клиента '%s': %s", client_data.get('name'), e, exc_info=True)
            raise

    def update_client(self, client_id: int, client_data: Dict[str, Any]) -> None:
        """Обновление данных клиента.

        Args:
            client_id: ID клиента.
            client_data: Словарь с обновлёнными данными.

        Raises:
            sqlite3.Error: При ошибке записи в БД.
        """
        try:
            with self.db._lock:
                self.db.cursor.execute('''
                    UPDATE clients
                    SET name=?, telegram=?, birth_date=?, destiny_number=?, matrix_id=?,
                        service_name=?, service_price=?, comment=?, phone=?, order_date=?
                    WHERE id=?
                ''', (
                    client_data['name'],
                    client_data.get('telegram'),
                    client_data['birth_date'],
                    client_data['destiny_number'],
                    client_data.get('matrix_id'),
                    client_data['service_name'],
                    client_data['service_price'],
                    client_data.get('comment'),
                    client_data.get('phone'),
                    client_data['order_date'],
                    client_id,
                ))
                self.db.conn.commit()
            logger.info("Обновлён клиент ID %d", client_id)
        except Exception as e:
            logger.error("Ошибка обновления клиента ID %d: %s", client_id, e, exc_info=True)
            raise

    def delete_client(self, client_id: int) -> None:
        """Удаление клиента по ID.

        Args:
            client_id: ID удаляемого клиента.

        Raises:
            sqlite3.Error: При ошибке удаления из БД.
        """
        with self.db._lock:
            self.db.cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
            self.db.conn.commit()
        logger.info("Удалён клиент ID %d", client_id)

    def get_all_clients(self) -> List[Client]:
        """Получение всех клиентов с названиями матриц.

        Returns:
            Список клиентов, отсортированных по дате создания (новые первыми).
        """
        with self.db._lock:
            self.db.cursor.execute('''
                SELECT clients.*, matrices.name as matrix_name
                FROM clients
                LEFT JOIN matrices ON clients.matrix_id = matrices.id
                ORDER BY clients.created_date DESC
            ''')
            rows = self.db.cursor.fetchall()
        clients = [Client.from_db_row(row) for row in rows]
        logger.debug("Загружено клиентов: %d", len(clients))
        return clients

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Получение клиента по ID вместе с названием матрицы.

        Args:
            client_id: ID клиента.

        Returns:
            Объект Client или None, если клиент не найден.
        """
        with self.db._lock:
            self.db.cursor.execute('''
                SELECT clients.*, matrices.name as matrix_name
                FROM clients
                LEFT JOIN matrices ON clients.matrix_id = matrices.id
                WHERE clients.id = ?
            ''', (client_id,))
            row = self.db.cursor.fetchone()
        if not row:
            logger.warning("Клиент ID %d не найден", client_id)
            return None
        client = Client.from_db_row(row)
        logger.debug("Получен клиент ID %d: %s", client_id, client.name)
        return client

    def toggle_completed(self, client_id: int) -> bool:
        """Переключение статуса выполнения заказа.

        Args:
            client_id: ID клиента.

        Returns:
            Новый статус выполнения (True — выполнен).
        """
        with self.db._lock:
            self.db.cursor.execute(
                'SELECT is_completed FROM clients WHERE id = ?', (client_id,)
            )
            result = self.db.cursor.fetchone()
            if not result:
                logger.warning("toggle_completed: клиент ID %d не найден", client_id)
                return False

            new_status = 0 if result['is_completed'] else 1
            completed_date = datetime.now().strftime("%d.%m.%Y") if new_status == 1 else None

            self.db.cursor.execute(
                'UPDATE clients SET is_completed=?, completed_date=? WHERE id=?',
                (new_status, completed_date, client_id),
            )
            self.db.conn.commit()

        logger.info(
            "Клиент ID %d отмечен как %s",
            client_id,
            "выполнен" if new_status else "не выполнен",
        )
        return bool(new_status)