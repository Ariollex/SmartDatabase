# -*- mode: python ; coding: utf-8 -*-
from main import version
import platform

#
# Parameters
#
onefile = True
block_cipher = None


#
# Main spec file elements
#
a = Analysis(
        ['main.py'],
        pathex=[],
        binaries=[],
        datas=[],
        hiddenimports=[],
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=True,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=True,
    )

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
        pyz,
        a.scripts,
        a.binaries if onefile else [],
        a.zipfiles if onefile else [],
        a.datas if onefile else [],
        exclude_binaries=not onefile,
        name='Extras',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=True,
        argv_emulation=True,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        version='version_file.txt',
    )
bundle_obj = exe
