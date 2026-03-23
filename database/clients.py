# -*- coding: utf-8 -*-

"""Работа с клиентами в БД"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from database.models import Client
from database.utils import calculate_destiny_number


class ClientsDB:
    """Класс для работы с клиентами"""
    
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor
        self.conn = db.conn
    
    def add_client(self, client_data: Dict[str, Any]) -> int:
        """Добавление нового клиента"""
        try:
            self.cursor.execute('''
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
                0, None
            ))
            self.conn.commit()
            client_id = self.cursor.lastrowid
            print(f"✅ Добавлен клиент: {client_data['name']} (ID: {client_id})")
            return client_id
        except Exception as e:
            print(f"❌ Ошибка добавления клиента: {e}")
            raise
    
    def update_client(self, client_id: int, client_data: Dict[str, Any]):
        """Обновление данных клиента"""
        try:
            self.cursor.execute('''
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
                client_id
            ))
            self.conn.commit()
            print(f"✅ Обновлен клиент ID {client_id}")
        except Exception as e:
            print(f"❌ Ошибка обновления клиента: {e}")
            raise
    
    def delete_client(self, client_id: int):
        """Удаление клиента по ID"""
        self.cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
        self.conn.commit()
        print(f"✅ Удален клиент ID {client_id}")
    
    def get_all_clients(self) -> List[Client]:
        """Получение всех клиентов с названиями матриц"""
        self.cursor.execute('''
            SELECT clients.*, matrices.name as matrix_name
            FROM clients 
            LEFT JOIN matrices ON clients.matrix_id = matrices.id 
            ORDER BY clients.created_date DESC
        ''')
        rows = self.cursor.fetchall()
        clients = []
        
        print("\n🔍 ВСЕ КЛИЕНТЫ В БАЗЕ:")
        for row in rows:
            client = Client.from_db_row(row)
            clients.append(client)
            print(f"  ID: {client.id}")
            print(f"  Имя: '{client.name}'")
            print(f"  Телефон: '{client.phone}'")
            print(f"  Telegram: '{client.telegram}'")
            print(f"  Комментарий: '{client.comment}'")
            print(f"  ---")
        
        print(f"📊 Всего клиентов: {len(clients)}")
        return clients
    
    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Получение клиента по ID"""
        self.cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
        row = self.cursor.fetchone()
        if row:
            # Получаем название матрицы отдельно
            matrix_name = None
            if row[5]:  # matrix_id
                self.cursor.execute('SELECT name FROM matrices WHERE id = ?', (row[5],))
                matrix_row = self.cursor.fetchone()
                matrix_name = matrix_row[0] if matrix_row else None
            
            # Преобразуем row в кортеж с matrix_name
            row_list = list(row)
            row_list.append(matrix_name)
            client = Client.from_db_row(tuple(row_list))
            print(f"✅ Получен клиент ID {client_id}: {client.name}")
            return client
        print(f"⚠️ Клиент ID {client_id} не найден")
        return None
    
    def toggle_completed(self, client_id: int) -> bool:
        """Переключение статуса выполнения заказа"""
        self.cursor.execute('SELECT is_completed FROM clients WHERE id = ?', (client_id,))
        result = self.cursor.fetchone()
        if not result:
            print(f"⚠️ Клиент ID {client_id} не найден")
            return False
        
        current = result[0]
        new_status = 1 if current == 0 else 0
        completed_date = datetime.now().strftime("%d.%m.%Y") if new_status == 1 else None
        
        self.cursor.execute('''
            UPDATE clients 
            SET is_completed=?, completed_date=?
            WHERE id=?
        ''', (new_status, completed_date, client_id))
        self.conn.commit()
        
        status_text = "выполнен" if new_status == 1 else "не выполнен"
        print(f"✅ Клиент ID {client_id} отмечен как {status_text}")
        
        return bool(new_status)