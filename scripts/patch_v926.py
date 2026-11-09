#!/usr/bin/env python3
"""Patch v925 -> v926: desktop chirp panel no longer pushes the compose box down on every send. The sticky
side panel (.comments-shell, not the phone preview/full-screen modes) was height:auto up to the screen
height, so in a short chat the chat area grew ~80px per chirp and the compose box slid down and off screen.
It's now always the full available height: compose box fixed at the bottom, chirps stack up above it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v925.js'
dst = '_deploy/assets/index-DUcNPOLc-v926.js'
content = open(src, encoding='utf-8').read()
old = '.comments-shell.chat-preview{position:static;max-height:none}'
new = '.comments-shell:not(.chat-preview):not(.chat-full){height:calc(100dvh - 91px)}' + old
if content.count(old) != 1: print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
