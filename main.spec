# -*- mode: python ; coding: utf-8 -*-
import sys
import platform
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# --- Detect Platform ---
current_system = platform.system()

# Include Tesseract binaries depending on platform
if current_system == "Windows":
    datas = [('Tesseract-OCR', 'Tesseract-OCR')]  # include Windows Tesseract folder
    argv_emulation = False
elif current_system == "Darwin":
    datas = [('Tesseract-OCR', 'Tesseract-OCR')]  # include macOS Tesseract folder if you have one
    argv_emulation = True
else:
    datas = []
    argv_emulation = False

# ------------------ Analysis ------------------
a = Analysis(
    ['main.py'],               # your main script
    pathex=[],                 # optional: add paths to your project if needed
    binaries=[],               # optional binaries
    datas=datas,               # included data (Tesseract)
    hiddenimports=[],          # optional: add hidden imports if PyInstaller misses any
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# ------------------ PYZ ------------------
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# ------------------ Executable ------------------
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BudgetBuddy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,             # ensures GUI-only mode
    disable_windowed_traceback=False,
    argv_emulation=argv_emulation,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ------------------ Collect ------------------
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BudgetBuddy',
)
