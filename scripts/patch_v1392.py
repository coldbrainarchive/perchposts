#!/usr/bin/env python3
"""Patch v1391 -> v1392: tapping the chat below an open post closes it too (was huddles only)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1391.js'
dst = '_deploy/assets/index-DUcNPOLc-v1392.js'
c = open(src, encoding='utf-8').read()
old = "children:[dock.post.is_huddle?(0,L.jsx)(`div`,{ref:BD,className:`ch-xp-bd`,onClick:ev=>{ev.stopPropagation();shut()}},`bd`):null,"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "children:[(0,L.jsx)(`div`,{ref:BD,className:`ch-xp-bd`,onClick:ev=>{ev.stopPropagation();shut()}},`bd`),"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
