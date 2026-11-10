#!/usr/bin/env python3
"""Patch v970 -> v971: no in-between width. The pinned desktop message box now applies whenever the chat is
the desktop panel (not the phone preview / full-screen chat), so it switches at the same width as the
phone layout (768px) instead of its own 901px."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v970.js'
dst = '_deploy/assets/index-DUcNPOLc-v971.js'
c = open(src, encoding='utf-8').read()
old = 'on=!!(sh&&mq.matches&&sh.querySelector(`.chat-compose`))'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, 'on=!!(sh&&sh.querySelector(`.chat-compose`))')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
