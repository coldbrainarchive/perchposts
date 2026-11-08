#!/usr/bin/env python3
"""Patch v95 -> v96: fix invalid CSS colors in signup pill.
hsl() strings can't have hex digits appended — use valid hsla() instead.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v95.js'
dst = '_deploy/assets/index-DUcNPOLc-v96.js'

content = open(src, encoding='utf-8').read()
errors = []

# Helper: Hn() returns "hsl(i, 72%, 68%)" — convert to hsla via string replace
# We use an inline JS expression:
#   Hn(null,_gu).replace('hsl(','hsla(').replace(')',', 0.12)')
HSLA = "Hn(null,_gu).replace('hsl(','hsla(').replace(')',', 0.12)')"

# ── 1. Fix border: use solid hsl color directly (no transparency needed) ──────
OLD_BORDER = 'border:_gu?`1.5px solid ${Hn(null,_gu)}55`:`1.5px dashed #3f4756`'
NEW_BORDER = 'border:_gu?`1.5px solid ${Hn(null,_gu)}`:`1.5px dashed #3f4756`'
if OLD_BORDER in content:
    content = content.replace(OLD_BORDER, NEW_BORDER, 1)
    print('OK: border now uses solid hsl color')
else:
    errors.append('FAIL: border pattern not found')

# ── 2. Fix background: convert hsl -> hsla with 0.12 alpha ───────────────────
OLD_BG = 'background:_gu?`${Hn(null,_gu)}18`:`transparent`'
NEW_BG = f'background:_gu?{HSLA}:`transparent`'
if OLD_BG in content:
    content = content.replace(OLD_BG, NEW_BG, 1)
    print('OK: background now uses hsla(0.12)')
else:
    errors.append('FAIL: background pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
