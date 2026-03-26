"""
Nuitka build script — compiles Python to C for fastest possible startup.

Usage:
    pip install nuitka ordered-set zstandard
    python build_nuitka.py

Nuitka produces a standalone folder similar to PyInstaller --onedir,
but the code runs as compiled C, not interpreted Python — significantly
faster startup and execution.
"""

import subprocess
import sys


def build() -> None:
    cmd = [
        sys.executable, "-m", "nuitka",
        # Standalone: bundle all dependencies
        "--standalone",
        # Windowed: no console
        "--windows-disable-console",
        # Output directory
        "--output-dir=dist_nuitka",
        "--output-filename=ClientManager.exe",
        # Include PySide6 plugin (handles Qt plugins/dlls automatically)
        "--enable-plugin=pyside6",
        # Data files
        "--include-data-dir=themes=themes",
        "--include-data-dir=config=config",
        # Exclude unused heavy Qt modules
        "--nofollow-import-to=PySide6.Qt3DAnimation",
        "--nofollow-import-to=PySide6.Qt3DCore",
        "--nofollow-import-to=PySide6.Qt3DExtras",
        "--nofollow-import-to=PySide6.Qt3DInput",
        "--nofollow-import-to=PySide6.Qt3DLogic",
        "--nofollow-import-to=PySide6.Qt3DRender",
        "--nofollow-import-to=PySide6.QtBluetooth",
        "--nofollow-import-to=PySide6.QtCharts",
        "--nofollow-import-to=PySide6.QtDataVisualization",
        "--nofollow-import-to=PySide6.QtDesigner",
        "--nofollow-import-to=PySide6.QtHelp",
        "--nofollow-import-to=PySide6.QtHttpServer",
        "--nofollow-import-to=PySide6.QtLocation",
        "--nofollow-import-to=PySide6.QtMultimedia",
        "--nofollow-import-to=PySide6.QtMultimediaWidgets",
        "--nofollow-import-to=PySide6.QtNetwork",
        "--nofollow-import-to=PySide6.QtNetworkAuth",
        "--nofollow-import-to=PySide6.QtNfc",
        "--nofollow-import-to=PySide6.QtOpenGL",
        "--nofollow-import-to=PySide6.QtOpenGLWidgets",
        "--nofollow-import-to=PySide6.QtPdf",
        "--nofollow-import-to=PySide6.QtPdfWidgets",
        "--nofollow-import-to=PySide6.QtPositioning",
        "--nofollow-import-to=PySide6.QtPrintSupport",
        "--nofollow-import-to=PySide6.QtQml",
        "--nofollow-import-to=PySide6.QtQuick",
        "--nofollow-import-to=PySide6.QtQuick3D",
        "--nofollow-import-to=PySide6.QtQuickControls2",
        "--nofollow-import-to=PySide6.QtQuickWidgets",
        "--nofollow-import-to=PySide6.QtRemoteObjects",
        "--nofollow-import-to=PySide6.QtScxml",
        "--nofollow-import-to=PySide6.QtSensors",
        "--nofollow-import-to=PySide6.QtSerialBus",
        "--nofollow-import-to=PySide6.QtSerialPort",
        "--nofollow-import-to=PySide6.QtSpatialAudio",
        "--nofollow-import-to=PySide6.QtSql",
        "--nofollow-import-to=PySide6.QtStateMachine",
        "--nofollow-import-to=PySide6.QtSvg",
        "--nofollow-import-to=PySide6.QtSvgWidgets",
        "--nofollow-import-to=PySide6.QtTest",
        "--nofollow-import-to=PySide6.QtTextToSpeech",
        "--nofollow-import-to=PySide6.QtUiTools",
        "--nofollow-import-to=PySide6.QtWebChannel",
        "--nofollow-import-to=PySide6.QtWebEngine",
        "--nofollow-import-to=PySide6.QtWebEngineCore",
        "--nofollow-import-to=PySide6.QtWebEngineQuick",
        "--nofollow-import-to=PySide6.QtWebEngineWidgets",
        "--nofollow-import-to=PySide6.QtWebSockets",
        "--nofollow-import-to=PySide6.QtXml",
        # Exclude stdlib modules not needed
        "--nofollow-import-to=tkinter",
        "--nofollow-import-to=unittest",
        "--nofollow-import-to=test",
        "--nofollow-import-to=lib2to3",
        "--nofollow-import-to=pydoc",
        "--nofollow-import-to=doctest",
        "--nofollow-import-to=multiprocessing",
        # Performance flags
        "--lto=yes",           # Link-time optimization
        "--jobs=4",            # Parallel compilation
        # Entry point
        "main.py",
    ]

    print("=" * 60)
    print("Building with Nuitka (Python -> C compilation)")
    print("=" * 60)
    print(" ".join(cmd[:6]), "...")
    print()

    result = subprocess.run(cmd, cwd=".")
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("Build successful! Output: dist_nuitka/main.dist/")
        print("=" * 60)
    else:
        print("Build failed with code", result.returncode)
        sys.exit(result.returncode)


if __name__ == "__main__":
    build()
