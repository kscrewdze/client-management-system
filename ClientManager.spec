# -*- mode: python ; coding: utf-8 -*-

"""
Optimized PyInstaller spec — ONE-DIR mode for fast startup.

Usage:
    pyinstaller ClientManager.spec

Key optimizations vs --onefile:
  - --onedir: files already on disk, no extraction on every launch (~10x faster start)
  - Explicit PySide6 excludes: drop unused Qt modules (~50-70% smaller bundle)
  - UPX compression for smaller binaries
"""

import os
import sys

block_cipher = None

# ── Paths ──────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(SPEC))
OUTPUT_DIR = os.path.join(HERE, "output")
DIST_DIR = os.path.join(OUTPUT_DIR, "dist")
BUILD_DIR = os.path.join(OUTPUT_DIR, "build")

# ── Excluded PySide6 modules (not used by the app) ────────────────
_pyside6_excludes = [
    "PySide6.Qt3DAnimation",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DExtras",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic",
    "PySide6.Qt3DRender",
    "PySide6.QtBluetooth",
    "PySide6.QtCharts",
    "PySide6.QtConcurrent",
    "PySide6.QtDataVisualization",
    "PySide6.QtDesigner",
    "PySide6.QtHelp",
    "PySide6.QtHttpServer",
    "PySide6.QtLocation",
    "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets",
    "PySide6.QtNetwork",
    "PySide6.QtNetworkAuth",
    "PySide6.QtNfc",
    "PySide6.QtOpenGL",
    "PySide6.QtOpenGLWidgets",
    "PySide6.QtPdf",
    "PySide6.QtPdfWidgets",
    "PySide6.QtPositioning",
    "PySide6.QtPrintSupport",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuick3D",
    "PySide6.QtQuickControls2",
    "PySide6.QtQuickWidgets",
    "PySide6.QtRemoteObjects",
    "PySide6.QtScxml",
    "PySide6.QtSensors",
    "PySide6.QtSerialBus",
    "PySide6.QtSerialPort",
    "PySide6.QtSpatialAudio",
    "PySide6.QtSql",
    "PySide6.QtStateMachine",
    "PySide6.QtSvg",
    "PySide6.QtSvgWidgets",
    "PySide6.QtTest",
    "PySide6.QtTextToSpeech",
    "PySide6.QtUiTools",
    "PySide6.QtWebChannel",
    "PySide6.QtWebEngine",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineQuick",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebSockets",
    "PySide6.QtXml",
]

_other_excludes = [
    "tkinter",
    "customtkinter",
    "unittest",
    "test",
    "email",
    "html",
    "http",
    "xmlrpc",
    "pydoc",
    "doctest",
    "lib2to3",
    "multiprocessing",
]

excludes = _pyside6_excludes + _other_excludes

# ── Analysis ──────────────────────────────────────────────────────
a = Analysis(
    [os.path.join(HERE, "main.py")],
    pathex=[HERE],
    binaries=[],
    datas=[
        (os.path.join(HERE, "themes"), "themes"),
        (os.path.join(HERE, "config"), "config"),
        (os.path.join(HERE, "icon.ico"), "."),
    ],
    hiddenimports=[
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "shiboken6",
        "openpyxl",
        "python_dateutil",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=2,             # Python -OO (remove docstrings + asserts)
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ── ONE-DIR EXE (fast startup) ───────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # This makes it --onedir
    name="ClientManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # --windowed
    icon=os.path.join(HERE, "icon.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ClientManager",
)
