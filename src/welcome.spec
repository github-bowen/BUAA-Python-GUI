# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['frontend/welcome.py'],
    ['frontend/addTask.py'],
    ['frontend/caledndarFront.py'],
    ['frontend/changeStyle.py'],
    ['frontend/editTask.py'],
    ['frontend/login.py'],
    ['frontend/passwordEdit.py'],
    ['frontend/taskDisplay.py'],
    ['frontend/taskLabel.py'],
    pathex=['/home/normalller/data/files/ImportantFile/LearningFiles/2_3/python(全英文)/2022Python大作业/calendar],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='welcome',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
