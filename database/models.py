# -*- coding: utf-8 -*-

"""Модели данных"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any, Dict


@dataclass
class Matrix:
    """Модель матрицы"""
    id: Optional[int]
    name: str
    price: float
    created_date: str
    
    @classmethod
    def from_db_row(cls, row: Any) -> 'Matrix':
        """Создание из строки БД"""
        return cls(
            id=row[0],
            name=row[1],
            price=row[2],
            created_date=row[3]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'created_date': self.created_date
        }


@dataclass
class Client:
    """Модель клиента"""
    id: Optional[int]
    name: str
    telegram: Optional[str]
    birth_date: str
    destiny_number: int
    matrix_id: Optional[int]
    service_name: str
    service_price: float
    comment: Optional[str]
    phone: Optional[str]
    order_date: str
    created_date: str
    is_completed: bool
    completed_date: Optional[str]
    matrix_name: Optional[str] = None
    
    @classmethod
    def from_db_row(cls, row: Any) -> 'Client':
        """Создание из строки БД"""
        # Определяем длину кортежа для обратной совместимости
        if len(row) >= 15:
            return cls(
                id=row[0],
                name=row[1],
                telegram=row[2],
                birth_date=row[3],
                destiny_number=row[4],
                matrix_id=row[5],
                service_name=row[6],
                service_price=row[7],
                comment=row[8],
                phone=row[9],
                order_date=row[10],
                created_date=row[11],
                is_completed=bool(row[12]),
                completed_date=row[13],
                matrix_name=row[14]
            )
        else:
            return cls(
                id=row[0],
                name=row[1],
                telegram=row[2],
                birth_date=row[3],
                destiny_number=row[4],
                matrix_id=row[5],
                service_name=row[6],
                service_price=row[7],
                comment=row[8] if len(row) > 8 else None,
                phone=row[9] if len(row) > 9 else None,
                order_date=row[10] if len(row) > 10 else row[3],
                created_date=row[11] if len(row) > 11 else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_completed=bool(row[12]) if len(row) > 12 else False,
                completed_date=row[13] if len(row) > 13 else None,
                matrix_name=row[14] if len(row) > 14 else None
            )
    
    @property
    def formatted_price(self) -> str:
        """Форматированная цена"""
        return f"{self.service_price:,.0f} руб.".replace(",", " ")
    
    @property
    def status_emoji(self) -> str:
        """Эмодзи статуса"""
        return "✅" if self.is_completed else "⏳"
    
    @property
    def status_text(self) -> str:
        """Текст статуса"""
        return "Выполнен" if self.is_completed else "В ожидании"
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'telegram': self.telegram,
            'birth_date': self.birth_date,
            'destiny_number': self.destiny_number,
            'matrix_id': self.matrix_id,
            'matrix_name': self.matrix_name,
            'service_name': self.service_name,
            'service_price': self.service_price,
            'comment': self.comment,
            'phone': self.phone,
            'order_date': self.order_date,
            'created_date': self.created_date,
            'is_completed': self.is_completed,
            'completed_date': self.completed_date,
            'status': self.status_text
        }