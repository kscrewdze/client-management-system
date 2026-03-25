# -*- coding: utf-8 -*-

"""Тесты валидаторов и парсера дат"""
import pytest
from datetime import datetime

from utils.validators import Validators
from utils.date_parser import DateParser
from database.utils import calculate_destiny_number


class TestValidateName:
    """Валидация имён."""

    def test_valid_name(self):
        ok, msg = Validators.validate_name("Иван Петров")
        assert ok is True
        assert msg == ""

    def test_empty_name(self):
        ok, msg = Validators.validate_name("")
        assert ok is False

    def test_none_name(self):
        ok, msg = Validators.validate_name(None)
        assert ok is False

    def test_whitespace_only(self):
        ok, msg = Validators.validate_name("   ")
        assert ok is False

    def test_too_short(self):
        ok, msg = Validators.validate_name("A")
        assert ok is False

    def test_too_long(self):
        ok, msg = Validators.validate_name("A" * 101)
        assert ok is False

    def test_forbidden_chars(self):
        ok, _ = Validators.validate_name("Test<script>")
        assert ok is False

    def test_two_chars(self):
        ok, _ = Validators.validate_name("Яя")
        assert ok is True


class TestValidatePhone:
    """Валидация телефона."""

    def test_valid_phone(self):
        ok, msg = Validators.validate_phone("+79001234567")
        assert ok is True

    def test_empty_phone_allowed(self):
        ok, _ = Validators.validate_phone("")
        assert ok is True

    def test_none_phone_allowed(self):
        ok, _ = Validators.validate_phone(None)
        assert ok is True

    def test_too_short(self):
        ok, _ = Validators.validate_phone("123")
        assert ok is False

    def test_too_long(self):
        ok, _ = Validators.validate_phone("+" + "1" * 20)
        assert ok is False

    def test_phone_with_formatting(self):
        ok, _ = Validators.validate_phone("+7 (900) 123-45-67")
        assert ok is True


class TestValidatePrice:
    """Валидация цены."""

    def test_valid_float(self):
        ok, msg, val = Validators.validate_price("1500.50")
        assert ok is True
        assert val == 1500.50

    def test_valid_int(self):
        ok, _, val = Validators.validate_price("5000")
        assert ok is True
        assert val == 5000.0

    def test_comma_separator(self):
        ok, _, val = Validators.validate_price("1500,50")
        assert ok is True
        assert val == 1500.50

    def test_empty_price(self):
        ok, _, _ = Validators.validate_price("")
        assert ok is False

    def test_negative_price(self):
        ok, _, _ = Validators.validate_price("-100")
        assert ok is False

    def test_too_large(self):
        ok, _, _ = Validators.validate_price("99999999")
        assert ok is False

    def test_not_a_number(self):
        ok, _, _ = Validators.validate_price("abc")
        assert ok is False

    def test_numeric_input(self):
        ok, _, val = Validators.validate_price(3000)
        assert ok is True
        assert val == 3000.0

    def test_zero_price(self):
        ok, _, val = Validators.validate_price("0")
        assert ok is True
        assert val == 0.0


class TestValidateTelegram:
    """Валидация Telegram username."""

    def test_valid_username(self):
        ok, _ = Validators.validate_telegram("@ivan_test")
        assert ok is True

    def test_valid_without_at(self):
        ok, _ = Validators.validate_telegram("ivan_test")
        assert ok is True

    def test_empty_allowed(self):
        ok, _ = Validators.validate_telegram("")
        assert ok is True

    def test_none_allowed(self):
        ok, _ = Validators.validate_telegram(None)
        assert ok is True

    def test_too_short(self):
        ok, _ = Validators.validate_telegram("@ab")
        assert ok is False

    def test_invalid_chars(self):
        ok, _ = Validators.validate_telegram("@иван")
        assert ok is False


class TestValidateDate:
    """Валидация дат."""

    def test_valid_date(self):
        ok, _, dt = Validators.validate_date("26.01.1982")
        assert ok is True
        assert dt.year == 1982

    def test_empty_date(self):
        ok, _, _ = Validators.validate_date("")
        assert ok is False

    def test_invalid_format(self):
        ok, _, _ = Validators.validate_date("not-a-date")
        assert ok is False

    def test_too_old(self):
        ok, _, _ = Validators.validate_date("01.01.1800")
        assert ok is False


class TestDateParser:
    """Тесты DateParser."""

    def test_dd_mm_yyyy(self):
        dt = DateParser.parse("26.01.1982")
        assert dt == datetime(1982, 1, 26)

    def test_dd_mm_yy(self):
        dt = DateParser.parse("26.01.82")
        assert dt is not None
        assert dt.day == 26

    def test_slash_format(self):
        dt = DateParser.parse("26/01/1982")
        assert dt == datetime(1982, 1, 26)

    def test_dash_format(self):
        dt = DateParser.parse("26-01-1982")
        assert dt == datetime(1982, 1, 26)

    def test_no_separators(self):
        """Формат ДДММГГГГ без разделителей."""
        dt = DateParser.parse("26011982")
        assert dt == datetime(1982, 1, 26)

    def test_invalid_returns_none(self):
        assert DateParser.parse("") is None
        assert DateParser.parse(None) is None
        assert DateParser.parse("абвгд") is None

    def test_format_date(self):
        dt = datetime(2025, 6, 15)
        assert DateParser.format_date(dt) == "15.06.2025"

    def test_get_month_name(self):
        assert DateParser.get_month_name(1) == "Январь"
        assert DateParser.get_month_name(12) == "Декабрь"

    def test_get_month_name_invalid(self):
        result = DateParser.get_month_name(13)
        assert "13" in result  # fallback


class TestDestinyNumber:
    """Тесты числа судьбы."""

    @pytest.mark.parametrize("birth_date,expected", [
        ("26.01.1982", 11),   # 2+6+0+1+1+9+8+2=29→2+9=11
        ("01.01.2000", 4),    # 0+1+0+1+2+0+0+0=4
        ("31.12.1999", 8),    # 3+1+1+2+1+9+9+9=35→3+5=8
        ("15.05.1990", 3),    # 1+5+0+5+1+9+9+0=30→3+0=3
        ("22.11.2001", 9),    # 2+2+1+1+2+0+0+1=9
    ])
    def test_calculate(self, birth_date, expected):
        result = calculate_destiny_number(birth_date)
        assert result == expected

    def test_empty_string(self):
        assert calculate_destiny_number("") == 0

    def test_invalid_string(self):
        assert calculate_destiny_number("абвгд") == 0

    def test_no_separators(self):
        """Формат без разделителей."""
        assert calculate_destiny_number("26011982") == 11
