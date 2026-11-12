#!/usr/bin/env python3
"""Patch v1032 -> v1033: a space between the emoji and the word in the full-screen tag pills ("📰 GENERAL")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1032.js'
dst = '_deploy/assets/index-DUcNPOLc-v1033.js'
c = open(src, encoding='utf-8').read()
old = 'const t=x.textContent.trim();if(!t||t.length>28)continue;'
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, 'const t=x.textContent.trim().replace(/^([^\\p{L}\\p{N}\\s]+)\\s*(?=[\\p{L}\\p{N}])/u,`$1 `);if(!t||t.length>30)continue;')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
