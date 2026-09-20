# optilux.spec — build recipe for PyInstaller

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = [
    "tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "PIL._tkinter_finder",
    "PIL.ImageTk",
    "PIL.ImageDraw",
    "reportlab.pdfgen",
    "reportlab.lib.pagesizes",
    "reportlab.lib.colors",
    "docx",
    "docx.shared",
    "docx.enum.text",
    "docx.enum.table",
    "docx.oxml.ns",
    "docx.oxml",
    "windows_toasts",
    "lxml.etree",
    "lxml._elementpath",
    "urllib.request",
    "winreg",
]

hiddenimports += collect_submodules("PIL")
hiddenimports += collect_submodules("reportlab")
hiddenimports += collect_submodules("docx")

datas = [
    ("modell2027.docx", "."),
    ("assets", "assets"),
]
datas += collect_data_files("reportlab")
datas += collect_data_files("docx")

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "numpy", "scipy", "pandas", "PyQt5", "PySide2"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Optilux",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/optilux.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Optilux",
)