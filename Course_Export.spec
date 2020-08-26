# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Course_Export.py'],
             pathex=['C:\\Users\\apope\\Documents\\Personal\\class_export'],
             binaries=[],
             datas=[('wingicon.ico', '.'), ('recurrent_ics/grammar/contentline.ebnf', 'recurrent_ics/grammar/')],
             hiddenimports=[],
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
          a.zipfiles,
          a.datas,
          [],
          name='Course_Export',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='wingicon.ico')
