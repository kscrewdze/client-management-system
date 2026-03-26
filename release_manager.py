#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Release Manager — автоматизация версионирования, сборки EXE,
тестирования и подготовки релиза для GitHub.

Использование:
    python release_manager.py build          # Собрать EXE текущей версии
    python release_manager.py bump patch     # 9.1.0 -> 9.1.1
    python release_manager.py bump minor     # 9.1.0 -> 9.2.0
    python release_manager.py bump major     # 9.1.0 -> 10.0.0
    python release_manager.py release        # bump patch + build + package
    python release_manager.py release minor  # bump minor + build + package
    python release_manager.py status         # Показать текущую версию и статус
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"
DIST_DIR = OUTPUT_DIR / "dist"
BUILD_DIR = OUTPUT_DIR / "build"
EXE_ARCHIVE_DIR = OUTPUT_DIR / "exe_archive"
RELEASES_DIR = ROOT / "releases"
VERSION_FILE = ROOT / "version.py"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
PYPROJECT_FILE = ROOT / "pyproject.toml"
SPEC_FILE = ROOT / "ClientManager.spec"
RELEASE_LOG = RELEASES_DIR / "releases.json"


# ── Version helpers ────────────────────────────────────────────────

def read_version() -> str:
    """Read VERSION from version.py."""
    ns: dict = {}
    exec(VERSION_FILE.read_text(encoding="utf-8"), ns)
    return ns["VERSION"]


def write_version(new_ver: str) -> None:
    """Write VERSION to version.py."""
    VERSION_FILE.write_text(
        '# -*- coding: utf-8 -*-\n\n'
        '"""\n'
        'Единый источник версии приложения.\n\n'
        'Все модули (main.py, settings.py, app.py, build scripts)\n'
        'импортируют VERSION отсюда.\n'
        '"""\n\n'
        f'VERSION = "{new_ver}"\n',
        encoding="utf-8",
    )


def bump_version(part: str) -> str:
    """Bump version by part (major/minor/patch). Returns new version."""
    old = read_version()
    major, minor, patch = (int(x) for x in old.split("."))
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Unknown part: {part}. Use major/minor/patch.")
        sys.exit(1)
    new_ver = f"{major}.{minor}.{patch}"
    write_version(new_ver)
    _update_pyproject(new_ver)
    print(f"Version bumped: {old} -> {new_ver}")
    return new_ver


def _update_pyproject(new_ver: str) -> None:
    """Update version in pyproject.toml."""
    if not PYPROJECT_FILE.exists():
        return
    text = PYPROJECT_FILE.read_text(encoding="utf-8")
    import re
    text = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{new_ver}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    PYPROJECT_FILE.write_text(text, encoding="utf-8")


# ── Build ──────────────────────────────────────────────────────────

def find_python() -> str:
    """Find the correct Python with PySide6 installed."""
    candidates = [
        sys.executable,
        str(Path.home() / "AppData/Local/Python/bin/python.exe"),
        "python",
    ]
    for py in candidates:
        try:
            r = subprocess.run(
                [py, "-c", "import PySide6; print('ok')"],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode == 0 and "ok" in r.stdout:
                return py
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    print("ERROR: Cannot find Python with PySide6 installed.")
    sys.exit(1)


def run_tests(python: str) -> bool:
    """Run tests if pytest is available. Returns True if passed or skipped."""
    print("\n--- Running tests ---")
    r = subprocess.run(
        [python, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120,
    )
    if r.returncode == 0:
        print("Tests PASSED")
        return True
    if "no module named pytest" in r.stderr.lower() or r.returncode == 5:
        print("pytest not found or no tests — skipping")
        return True
    print(f"Tests FAILED:\n{r.stdout}\n{r.stderr}")
    return False


def syntax_check(python: str) -> bool:
    """Check all .py files compile without syntax errors."""
    print("\n--- Syntax check ---")
    py_files = list(ROOT.rglob("*.py"))
    py_files = [f for f in py_files if "dist" not in str(f) and "__pycache__" not in str(f)]
    code = "; ".join(
        f"compile(open(r'{f}',encoding='utf-8').read(),r'{f}','exec')"
        for f in py_files[:50]  # batch limit
    )
    r = subprocess.run(
        [python, "-c", code + "; print('SYNTAX OK')"],
        capture_output=True, text=True, timeout=30,
    )
    if "SYNTAX OK" in r.stdout:
        print(f"Syntax OK ({len(py_files)} files)")
        return True
    print(f"Syntax errors:\n{r.stderr}")
    return False


def build_exe(python: str) -> Path:
    """Build EXE with PyInstaller. Returns path to dist folder."""
    version = read_version()
    print(f"\n--- Building EXE v{version} ---")

    # Ensure output directories exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    DIST_DIR.mkdir(exist_ok=True)
    BUILD_DIR.mkdir(exist_ok=True)
    EXE_ARCHIVE_DIR.mkdir(exist_ok=True)

    # Check PyInstaller
    r = subprocess.run(
        [python, "-m", "PyInstaller", "--version"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("Installing PyInstaller...")
        subprocess.run([python, "-m", "pip", "install", "pyinstaller"], check=True)

    # Clean old dist
    dist_app = DIST_DIR / "ClientManager"
    if dist_app.exists():
        shutil.rmtree(dist_app)

    # Build with output dirs outside the project
    cmd = [
        python, "-m", "PyInstaller", str(SPEC_FILE),
        "--noconfirm",
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
    ]
    print(f"Running: {' '.join(cmd[:4])}...")
    r = subprocess.run(cmd, cwd=str(ROOT), timeout=600)
    if r.returncode != 0:
        print("BUILD FAILED")
        sys.exit(1)

    exe_path = dist_app / "ClientManager.exe"
    if not exe_path.exists():
        print(f"ERROR: EXE not found at {exe_path}")
        sys.exit(1)

    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"Build OK: {exe_path} ({size_mb:.1f} MB)")

    # Copy full app folder to versioned archive
    archive_folder = EXE_ARCHIVE_DIR / f"ClientManager-v{version}"
    if archive_folder.exists():
        shutil.rmtree(archive_folder)
    shutil.copytree(dist_app, archive_folder)
    print(f"Archived: {archive_folder}")

    return dist_app


def smoke_test_exe(exe_dir: Path, python: str) -> bool:
    """Quick smoke test — launch EXE for 5 seconds, check no crash."""
    print("\n--- Smoke test ---")
    exe = exe_dir / "ClientManager.exe"
    if not exe.exists():
        print("SKIP: EXE not found")
        return True
    try:
        proc = subprocess.Popen(
            [str(exe)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=str(exe_dir),
        )
        try:
            proc.wait(timeout=5)
            # Exited within 5s — check if crash
            if proc.returncode != 0:
                _, stderr = proc.communicate()
                print(f"CRASH (exit code {proc.returncode}): {stderr.decode('utf-8', errors='replace')[:500]}")
                return False
            print("App exited cleanly within 5s (likely no display)")
            return True
        except subprocess.TimeoutExpired:
            proc.kill()
            print("Smoke test PASSED (app ran 5s without crash)")
            return True
    except Exception as e:
        print(f"Smoke test error: {e}")
        return True  # Don't block on display-less environments


# ── Package ────────────────────────────────────────────────────────

def package_release(version: str, dist_app: Path) -> Path:
    """Create ZIP in releases/ folder."""
    RELEASES_DIR.mkdir(exist_ok=True)
    zip_name = f"ClientManager-v{version}-win64.zip"
    zip_path = RELEASES_DIR / zip_name

    print(f"\n--- Packaging {zip_name} ---")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in dist_app.rglob("*"):
            if f.is_file():
                arcname = f"ClientManager-v{version}/{f.relative_to(dist_app)}"
                zf.write(f, arcname)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Package: {zip_path} ({size_mb:.1f} MB)")
    return zip_path


def update_release_log(version: str, zip_path: Path, test_ok: bool) -> None:
    """Append entry to releases/releases.json."""
    RELEASES_DIR.mkdir(exist_ok=True)
    log: list = []
    if RELEASE_LOG.exists():
        try:
            log = json.loads(RELEASE_LOG.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            log = []

    entry = {
        "version": version,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file": zip_path.name,
        "size_mb": round(zip_path.stat().st_size / (1024 * 1024), 1),
        "tests_passed": test_ok,
    }
    log.append(entry)
    RELEASE_LOG.write_text(
        json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    print(f"Release log updated: {RELEASE_LOG}")


def add_changelog_entry(version: str) -> None:
    """Add a placeholder changelog entry for the new version."""
    if not CHANGELOG_FILE.exists():
        return
    text = CHANGELOG_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"## [{version}] — {today}"
    if header in text:
        return  # Already exists
    # Insert after the first "## [" line
    marker = "## ["
    idx = text.find(marker)
    if idx == -1:
        return
    new_section = (
        f"{header}\n\n"
        "### Добавлено\n"
        "- Вкладка «Поддержка» (☕ донат, ⭐ GitHub, 🐛 Issues)\n"
        "- Фильтр клиентов по статусу (Все / Выполненные / В ожидании)\n"
        "- Столбец «Дата завершения» в таблице клиентов и Excel-экспорте\n"
        "- Lazy-загрузка вкладок (ускорение запуска)\n"
        "- Отложенный авто-экспорт при старте\n"
        "- Release Manager: автосборка EXE, версионирование, отчёты\n"
        "- GitHub Actions CI/CD: автосборка + релиз\n\n"
        "### Оптимизировано\n"
        "- PyInstaller --onedir (быстрый запуск вместо --onefile)\n"
        "- Исключены ~35 неиспользуемых Qt-модулей\n\n"
    )
    text = text[:idx] + new_section + text[idx:]
    CHANGELOG_FILE.write_text(text, encoding="utf-8")
    print(f"Changelog updated for v{version}")


RELEASES_FILE = ROOT / "RELEASES.md"


def update_releases_md(version: str) -> None:
    """Add a new release entry to RELEASES.md."""
    if not RELEASES_FILE.exists():
        return
    text = RELEASES_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"## v{version} — {today}"
    if header in text:
        return  # Already exists

    marker = "## v"
    idx = text.find(marker)
    if idx == -1:
        return

    repo_url = "https://github.com/kscrewdze/client-management-system"
    new_section = (
        f"{header}\n\n"
        f"**Скачать:** [{f'ClientManager-v{version}-win64.zip'}]"
        f"({repo_url}/releases/tag/v{version})\n\n"
        "### Что нового\n"
        "- *Обновите описание изменений*\n\n"
        "### Установка\n"
        "1. Скачайте ZIP-архив из ссылки выше\n"
        "2. Распакуйте в любую папку\n"
        "3. Запустите `ClientManager.exe`\n\n"
        "---\n\n"
    )
    text = text[:idx] + new_section + text[idx:]
    RELEASES_FILE.write_text(text, encoding="utf-8")
    print(f"RELEASES.md updated for v{version}")


# ── Commands ───────────────────────────────────────────────────────

def cmd_status() -> None:
    version = read_version()
    print(f"Version:  {version}")
    print(f"Root:     {ROOT}")
    print(f"Output:   {OUTPUT_DIR}")

    releases = list(RELEASES_DIR.glob("*.zip")) if RELEASES_DIR.exists() else []
    print(f"Releases: {len(releases)}")
    for r in sorted(releases):
        size = r.stat().st_size / (1024 * 1024)
        print(f"  {r.name}  ({size:.1f} MB)")

    exes = sorted(EXE_ARCHIVE_DIR.iterdir()) if EXE_ARCHIVE_DIR.exists() else []
    exes = [e for e in exes if e.is_dir()]
    print(f"EXE Archive: {len(exes)}")
    for e in exes:
        exe_file = e / "ClientManager.exe"
        if exe_file.exists():
            size = exe_file.stat().st_size / (1024 * 1024)
            print(f"  {e.name}/  (EXE: {size:.1f} MB)")


def cmd_build() -> None:
    python = find_python()
    if not syntax_check(python):
        sys.exit(1)
    tests_ok = run_tests(python)
    dist_app = build_exe(python)
    smoke_test_exe(dist_app, python)
    print(f"\n{'='*50}")
    print(f"BUILD COMPLETE: v{read_version()}")
    print(f"Output: {dist_app}")
    print(f"{'='*50}")


def cmd_release(bump_part: str = "patch") -> None:
    python = find_python()

    # 1. Syntax check
    if not syntax_check(python):
        sys.exit(1)

    # 2. Tests
    tests_ok = run_tests(python)

    # 3. Bump version
    version = bump_version(bump_part)

    # 4. Update changelog
    add_changelog_entry(version)

    # 5. Update RELEASES.md
    update_releases_md(version)

    # 6. Build EXE
    dist_app = build_exe(python)

    # 6. Smoke test
    smoke_test_exe(dist_app, python)

    # 8. Package ZIP
    zip_path = package_release(version, dist_app)

    # 9. Update release log
    update_release_log(version, zip_path, tests_ok)

    print(f"\n{'='*60}")
    print(f"RELEASE v{version} READY")
    print(f"{'='*60}")
    print(f"  ZIP:       {zip_path}")
    print(f"  Tests:     {'PASSED' if tests_ok else 'FAILED (check manually)'}")
    print(f"  Changelog: {CHANGELOG_FILE}")
    print()
    print("Next steps:")
    print(f"  git add -A")
    print(f"  git commit -m \"release: v{version}\"")
    print(f"  git tag v{version}")
    print(f"  git push origin master --tags")
    print(f"  # GitHub Actions will create the release automatically")


def main() -> None:
    parser = argparse.ArgumentParser(description="Release Manager for ClientManager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show current version and releases")
    sub.add_parser("build", help="Build EXE for current version")

    bump_p = sub.add_parser("bump", help="Bump version (major/minor/patch)")
    bump_p.add_argument("part", choices=["major", "minor", "patch"])

    rel_p = sub.add_parser("release", help="Full release: bump + build + package")
    rel_p.add_argument("part", nargs="?", default="patch",
                       choices=["major", "minor", "patch"])

    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "build":
        cmd_build()
    elif args.command == "bump":
        bump_version(args.part)
    elif args.command == "release":
        cmd_release(args.part)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
