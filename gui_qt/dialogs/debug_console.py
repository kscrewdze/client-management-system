# -*- coding: utf-8 -*-

"""
F12 Developer Console — terminal-style debug panel.
English UI with hacker aesthetic.
"""

import logging
import os
import platform
import sqlite3
import sys
import time
from datetime import datetime
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QFrame,
)

from version import VERSION

logger = logging.getLogger(__name__)

_CONSOLE_QSS = """
QDialog {
    background-color: #0a0e14;
}
QTextEdit {
    background-color: #0d1117;
    color: #00ff41;
    border: 1px solid #1a1f2b;
    selection-background-color: #1a3a1a;
    padding: 8px;
}
QLineEdit {
    background-color: #161b22;
    color: #00ff41;
    border: 1px solid #30363d;
    padding: 6px 8px;
    selection-background-color: #1a3a1a;
}
QLabel {
    color: #8b949e;
}
QPushButton {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    padding: 4px 12px;
    border-radius: 3px;
}
QPushButton:hover {
    background-color: #30363d;
    border-color: #8b949e;
}
QFrame#header {
    background-color: #161b22;
    border-bottom: 1px solid #21262d;
}
"""

_HELP_TEXT = """
[COMMANDS]
  help          — show this help
  status        — app status & diagnostics
  db <sql>      — execute raw SQL query
  tables        — list database tables
  count <tbl>   — row count for table
  schema <tbl>  — show CREATE TABLE statement
  env           — environment variables (filtered)
  mem           — memory usage
  clear         — clear console output
  exit          — close console

[SHORTCUTS]
  Enter         — execute command
  Ctrl+L        — clear console
  Up/Down       — (planned) command history
"""


class DebugConsoleDialog(QDialog):
    """F12 Developer Console with terminal-style interface."""

    def __init__(self, db: Any, parent=None) -> None:
        super().__init__(parent)
        self._db = db
        self._history: list[str] = []
        self._history_idx = 0

        self.setWindowTitle("F12 — Developer Console")
        self.setMinimumSize(750, 450)
        self.resize(950, 550)
        self.setWindowFlags(
            Qt.Dialog | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint
        )
        self.setStyleSheet(_CONSOLE_QSS)

        self._mono = QFont("Consolas", 10)
        if not self._mono.exactMatch():
            self._mono = QFont("Courier New", 10)

        self._build_ui()
        self._print_banner()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header bar
        hdr = QFrame()
        hdr.setObjectName("header")
        hdr.setFixedHeight(32)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(12, 0, 12, 0)

        title = QLabel("⌘ DEVELOPER CONSOLE")
        title.setStyleSheet("color: #58a6ff; font-weight: bold; font-size: 12px;")
        hl.addWidget(title)
        hl.addStretch()

        ver_lbl = QLabel(f"v{VERSION}  │  Python {platform.python_version()}  │  {platform.system()} {platform.release()}")
        ver_lbl.setStyleSheet("color: #484f58; font-size: 10px;")
        hl.addWidget(ver_lbl)

        clear_btn = QPushButton("Clear")
        clear_btn.setFixedHeight(22)
        clear_btn.clicked.connect(lambda: self._output.clear())
        hl.addWidget(clear_btn)

        root.addWidget(hdr)

        # Output area
        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setFont(self._mono)
        self._output.setLineWrapMode(QTextEdit.NoWrap)
        root.addWidget(self._output, stretch=1)

        # Input area
        inp_frame = QFrame()
        inp_frame.setStyleSheet("background: #0d1117; border-top: 1px solid #21262d;")
        il = QHBoxLayout(inp_frame)
        il.setContentsMargins(8, 4, 8, 4)

        prompt = QLabel("›")
        prompt.setStyleSheet("color: #00ff41; font-size: 16px; font-weight: bold;")
        prompt.setFont(self._mono)
        il.addWidget(prompt)

        self._input = QLineEdit()
        self._input.setFont(self._mono)
        self._input.setPlaceholderText("type 'help' for commands...")
        self._input.returnPressed.connect(self._on_enter)
        il.addWidget(self._input)

        root.addWidget(inp_frame)
        self._input.setFocus()

    # --- Output helpers ---

    def _print(self, text: str, color: str = "#c9d1d9") -> None:
        cursor = self._output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(f'<span style="color:{color};">{text}</span><br>')
        self._output.setTextCursor(cursor)
        self._output.ensureCursorVisible()

    def _print_banner(self) -> None:
        banner = (
            '<span style="color:#00ff41;">'
            "╔══════════════════════════════════════════════╗<br>"
            "║  CLIENT MANAGER — DEVELOPER CONSOLE          ║<br>"
            f"║  Version {VERSION:&lt;11s}│ Build {datetime.now().strftime('%Y-%m-%d'):&lt;14s}║<br>"
            "║  Type 'help' for available commands           ║<br>"
            "╚══════════════════════════════════════════════╝<br>"
            "</span>"
        )
        self._output.setHtml(f'<pre style="font-family: Consolas, monospace; font-size: 10pt;">{banner}</pre>')

    # --- Command execution ---

    def _on_enter(self) -> None:
        raw = self._input.text().strip()
        self._input.clear()
        if not raw:
            return

        self._history.append(raw)
        self._history_idx = len(self._history)
        self._print(f"<span style='color:#58a6ff;'>›</span> {_esc(raw)}", "#e6edf3")

        parts = raw.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "help":
                self._cmd_help()
            elif cmd == "status":
                self._cmd_status()
            elif cmd == "db":
                self._cmd_db(arg)
            elif cmd == "tables":
                self._cmd_tables()
            elif cmd == "count":
                self._cmd_count(arg)
            elif cmd == "schema":
                self._cmd_schema(arg)
            elif cmd == "env":
                self._cmd_env()
            elif cmd == "mem":
                self._cmd_mem()
            elif cmd == "clear":
                self._output.clear()
            elif cmd == "exit":
                self.close()
            else:
                self._print(f"Unknown command: '{_esc(cmd)}'. Type 'help'.", "#f85149")
        except Exception as e:
            self._print(f"ERROR: {_esc(str(e))}", "#f85149")

    def _cmd_help(self) -> None:
        for line in _HELP_TEXT.strip().split("\n"):
            self._print(_esc(line), "#8b949e")

    def _cmd_status(self) -> None:
        db_path = str(self._db.db_path)
        db_size = os.path.getsize(db_path) / 1024 if os.path.exists(db_path) else 0
        info = [
            f"App Version    : {VERSION}",
            f"Python         : {sys.version.split()[0]}",
            f"Platform       : {platform.platform()}",
            f"PID            : {os.getpid()}",
            f"Database       : {db_path}",
            f"DB Size        : {db_size:.1f} KB",
            f"SQLite Version : {sqlite3.sqlite3_version}",
            f"Working Dir    : {os.getcwd()}",
            f"Frozen         : {getattr(sys, 'frozen', False)}",
        ]
        for line in info:
            self._print(_esc(line), "#7ee787")

    def _cmd_db(self, sql: str) -> None:
        if not sql:
            self._print("Usage: db <SQL query>", "#f0883e")
            return
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT"):
            self._print("BLOCKED: only SELECT queries allowed in console.", "#f85149")
            return
        t0 = time.perf_counter()
        try:
            with self._db._lock:
                cursor = self._db.conn.execute(sql)
                if cursor.description:
                    headers = [d[0] for d in cursor.description]
                    rows = cursor.fetchall()
                    elapsed = (time.perf_counter() - t0) * 1000
                    self._print(f"  {' │ '.join(headers)}", "#58a6ff")
                    self._print(f"  {'─' * (len(headers) * 15)}", "#30363d")
                    for row in rows[:100]:
                        self._print(f"  {' │ '.join(_esc(str(v)) for v in row)}", "#c9d1d9")
                    if len(rows) > 100:
                        self._print(f"  ... and {len(rows) - 100} more rows", "#8b949e")
                    self._print(f"  [{len(rows)} rows in {elapsed:.1f}ms]", "#7ee787")
                else:
                    elapsed = (time.perf_counter() - t0) * 1000
                    self._print(f"  OK ({cursor.rowcount} affected, {elapsed:.1f}ms)", "#7ee787")
        except Exception as e:
            self._print(f"  SQL Error: {_esc(str(e))}", "#f85149")

    def _cmd_tables(self) -> None:
        try:
            with self._db._lock:
                cur = self._db.conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                tables = [r[0] for r in cur.fetchall()]
            for t in tables:
                with self._db._lock:
                    cnt = self._db.conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                self._print(f"  {t:30s} ({cnt} rows)", "#7ee787")
        except Exception as e:
            self._print(f"  Error: {_esc(str(e))}", "#f85149")

    def _cmd_count(self, table: str) -> None:
        if not table or not all(c.isalnum() or c == '_' for c in table):
            self._print("Usage: count <table_name>", "#f0883e")
            return
        try:
            with self._db._lock:
                cnt = self._db.conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            self._print(f"  {table}: {cnt} rows", "#7ee787")
        except Exception as e:
            self._print(f"  Error: {_esc(str(e))}", "#f85149")

    def _cmd_schema(self, table: str) -> None:
        if not table or not all(c.isalnum() or c == '_' for c in table):
            self._print("Usage: schema <table_name>", "#f0883e")
            return
        try:
            with self._db._lock:
                cur = self._db.conn.execute(
                    "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                    (table,),
                )
                row = cur.fetchone()
            if row:
                for line in row[0].split("\n"):
                    self._print(f"  {_esc(line)}", "#d2a8ff")
            else:
                self._print(f"  Table '{_esc(table)}' not found.", "#f85149")
        except Exception as e:
            self._print(f"  Error: {_esc(str(e))}", "#f85149")

    def _cmd_env(self) -> None:
        safe_keys = ["PATH", "APPDATA", "USERPROFILE", "TEMP", "COMPUTERNAME", "OS"]
        for key in safe_keys:
            val = os.environ.get(key, "N/A")
            self._print(f"  {key} = {_esc(val[:80])}", "#8b949e")

    def _cmd_mem(self) -> None:
        try:
            import psutil
            proc = psutil.Process(os.getpid())
            mem = proc.memory_info()
            self._print(f"  RSS  : {mem.rss / 1024 / 1024:.1f} MB", "#7ee787")
            self._print(f"  VMS  : {mem.vms / 1024 / 1024:.1f} MB", "#7ee787")
        except ImportError:
            # Fallback without psutil
            self._print("  psutil not installed — basic info only", "#f0883e")
            self._print(f"  PID    : {os.getpid()}", "#8b949e")
            self._print(f"  Frozen : {getattr(sys, 'frozen', False)}", "#8b949e")


def _esc(text: str) -> str:
    """Escape HTML entities for safe display."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
