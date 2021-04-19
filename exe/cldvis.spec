# -*- mode: python ; coding: utf-8 -*-
# filename = cldvis.spec
import os, glob

spec_root = os.path.abspath(os.path.join(SPECPATH, '..'))
datas = glob.glob(os.path.join('..', 'tda_mvc', 'icon', '*'))
datas = [(path, 'tda_mvc\\icon') for path in datas]

block_cipher = None
a = Analysis(['..\\app_mvc.py'],
             pathex=[spec_root],
             binaries=[],
             datas=datas,
             hiddenimports=['PySide.QtXml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          exclude_binaries=False,
          name='cldvis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='..\\tda_mvc\\icon\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='cldvis')
