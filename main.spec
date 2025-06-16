# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = BUNDLE(
    exe = EXE(
        script='main.py',
        name='Combine CSV',
        icon='icon.icns',  # Set your custom icon here
        windowed=True,
    ),
)
