# -*- coding: utf-8 -*-

"""Менеджер тем для приложения"""
import json
import os
from typing import Dict, Optional
import customtkinter as ctk
from datetime import datetime

from themes.themes.emerald import emerald
from themes.themes.sapphire import sapphire
from themes.themes.ruby import ruby
from themes.themes.amethyst import amethyst
from themes.themes.midnight import midnight
from themes.themes.sunrise import sunrise


class ThemeManager:
    """Менеджер тем приложения"""
    
    def __init__(self):
        self.themes = {
            "emerald": emerald,
            "sapphire": sapphire,
            "ruby": ruby,
            "amethyst": amethyst,
            "midnight": midnight,
            "sunrise": sunrise
        }
        self.current_theme = None
        self.config_file = os.path.join(os.path.dirname(__file__), 'theme_config.json')
        self.main_window = None
        
        # Загружаем сохраненную тему
        self.load_config()
        
        print(f"✅ ThemeManager инициализирован. Тем: {len(self.themes)}")
        if self.current_theme:
            print(f"📂 Текущая тема: {self.current_theme.name}")
    
    def set_main_window(self, main_window):
        """Установить ссылку на главное окно"""
        self.main_window = main_window
        print("🪟 Главное окно установлено")
        
        if self.current_theme:
            print(f"🎨 Применяю тему: {self.current_theme.name}")
            self._apply_theme(self.current_theme)
    
    def get_all_themes(self) -> Dict[str, str]:
        """Получить список всех тем с описаниями"""
        return {name: theme.description for name, theme in self.themes.items()}
    
    def get_theme(self, name: str):
        """Получить тему по имени"""
        return self.themes.get(name)
    
    def get_current_theme(self):
        """Получить текущую тему"""
        return self.current_theme
    
    def apply_theme(self, name: str) -> bool:
        """Применить тему"""
        print(f"🎨 Попытка применить тему: {name}")
        
        if name in self.themes:
            self.current_theme = self.themes[name]
            self._apply_theme(self.current_theme)
            self._save_config(name)
            print(f"✅ Тема '{self.current_theme.name}' применена")
            return True
        
        print(f"❌ Тема '{name}' не найдена")
        return False
    
    def _apply_theme(self, theme):
        """Применить тему к интерфейсу"""
        try:
            colors = theme.colors
            print(f"🎨 Применяю тему: {theme.name}")
            print(f"   Основной фон: {colors.background}")
            
            # Настройка режима
            if "Полуночная" in theme.name:
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
            
            # Применяем к главному окну
            if self.main_window:
                # Устанавливаем фон
                self.main_window.configure(fg_color=colors.background)
                
                # Обновляем основные цвета CustomTkinter
                ctk.set_default_color_theme("green")  # Базовый цвет
                
                self.main_window.update()
                print("   Тема применена")
            
        except Exception as e:
            print(f"❌ Ошибка применения темы: {e}")
    
    def _save_config(self, theme_name):
        """Сохранить настройки темы"""
        try:
            config = {'theme': theme_name, 'saved_at': datetime.now().isoformat()}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"💾 Тема сохранена: {theme_name}")
        except Exception as e:
            print(f"❌ Ошибка сохранения темы: {e}")
    
    def load_config(self):
        """Загрузить настройки темы"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    theme_name = data.get('theme')
                    if theme_name and theme_name in self.themes:
                        self.current_theme = self.themes[theme_name]
                        print(f"📂 Загружена тема: {theme_name}")
                    else:
                        print(f"📂 Тема {theme_name} не найдена, использую изумрудную")
                        self.current_theme = self.themes["emerald"]
            else:
                print("📂 Файл конфига не найден, использую изумрудную тему")
                self.current_theme = self.themes["emerald"]
        except Exception as e:
            print(f"❌ Ошибка загрузки темы: {e}")
            self.current_theme = self.themes["emerald"]


# Глобальный экземпляр
theme_manager = ThemeManager()