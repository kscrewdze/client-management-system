# -*- coding: utf-8 -*-

"""Фильтрация результатов поиска"""
from typing import List
from database.models import Client


class SearchFilters:
    """Класс для фильтрации результатов поиска"""
    
    @staticmethod
    def by_status(clients: List[Client], show_completed: bool = True, show_pending: bool = True) -> List[Client]:
        """
        Фильтрация клиентов по статусу выполнения
        
        Args:
            clients: список клиентов
            show_completed: показывать выполненные
            show_pending: показывать ожидающие
            
        Returns:
            List[Client]: отфильтрованный список
        """
        if show_completed and show_pending:
            return clients
        
        filtered = []
        for client in clients:
            if client.is_completed and show_completed:
                filtered.append(client)
            elif not client.is_completed and show_pending:
                filtered.append(client)
        
        return filtered
    
    @staticmethod
    def by_date_range(clients: List[Client], start_date: str = None, end_date: str = None) -> List[Client]:
        """
        Фильтрация по диапазону дат
        
        Args:
            clients: список клиентов
            start_date: начальная дата (включительно)
            end_date: конечная дата (включительно)
            
        Returns:
            List[Client]: отфильтрованный список
        """
        if not start_date and not end_date:
            return clients
        
        filtered = []
        for client in clients:
            if start_date and client.order_date < start_date:
                continue
            if end_date and client.order_date > end_date:
                continue
            filtered.append(client)
        
        return filtered
    
    @staticmethod
    def by_price_range(clients: List[Client], min_price: float = None, max_price: float = None) -> List[Client]:
        """
        Фильтрация по диапазону цен
        
        Args:
            clients: список клиентов
            min_price: минимальная цена
            max_price: максимальная цена
            
        Returns:
            List[Client]: отфильтрованный список
        """
        if min_price is None and max_price is None:
            return clients
        
        filtered = []
        for client in clients:
            if min_price is not None and client.service_price < min_price:
                continue
            if max_price is not None and client.service_price > max_price:
                continue
            filtered.append(client)
        
        return filtered
    
    @staticmethod
    def by_matrix(clients: List[Client], matrix_name: str = None) -> List[Client]:
        """
        Фильтрация по названию матрицы
        
        Args:
            clients: список клиентов
            matrix_name: название матрицы
            
        Returns:
            List[Client]: отфильтрованный список
        """
        if not matrix_name:
            return clients
        
        matrix_name_lower = matrix_name.lower()
        filtered = []
        for client in clients:
            if client.matrix_name and matrix_name_lower in client.matrix_name.lower():
                filtered.append(client)
        
        return filtered


# Создаем глобальный экземпляр
filters = SearchFilters()