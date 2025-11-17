# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app/main/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources/templates', 'resources/templates'),
        ('resources/images', 'resources/images'),
    ],
    hiddenimports=[
        'app',
        'app.main',
        'app.main.view',
        'app.config',
        'app.dto',
        'app.exception',
        'app.model',
        'app.repository',
        'app.service',
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.dialects.mysql',
        'sqlalchemy.dialects.postgresql',
        'pydantic',
        'jinja2',
        'weasyprint',
        'openpyxl',
        'slugify',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pacific-exporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='resources/images/icon.ico'  # Uncomment and add icon if you have one
)
