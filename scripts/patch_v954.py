#!/usr/bin/env python3
"""Patch v953 -> v954: pins in the chat are in chat order like the preview (oldest at the top, newest at
the bottom, next to the conversation)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v953.js'
dst = '_deploy/assets/index-DUcNPOLc-v954.js'
c = open(src, encoding='utf-8').read()
old = 'let _p2=[..._pins].sort((a,b)=>new Date(b.created_at)-new Date(a.created_at))'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, 'let _p2=[..._pins].sort((a,b)=>new Date(a.created_at)-new Date(b.created_at))')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
