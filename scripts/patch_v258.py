#!/usr/bin/env python3
"""Patch v257 -> v258: restore emojis on Hatch Date/Worm Count, cap card width for desktop."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v257.js'
dst = '_deploy/assets/index-DUcNPOLc-v258.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restore emojis on stat labels ─────────────────────────────────────────
replacements = [
    ('children:`HATCH DATE`', 'children:`\U0001f95a Hatch Date`'),
    ('children:`WORM COUNT`', 'children:`\U0001fab1 Worm Count`'),
]
for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'OK: {new[10:30]}')
    else:
        errors.append(f'FAIL: {old} not found')

# ── 2. Cap card width so it doesn't spread on desktop ────────────────────────
OLD_OUTER = 'style:{padding:`10px 14px`},children:[(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:14,border:`1px solid #2e303a`,overflow:`hidden`}'
NEW_OUTER = 'style:{padding:`10px 14px`,maxWidth:480,margin:`0 auto`},children:[(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:14,border:`1px solid #2e303a`,overflow:`hidden`}'
if OLD_OUTER in content:
    content = content.replace(OLD_OUTER, NEW_OUTER, 1)
    print('OK: card capped at 480px and centered')
else:
    errors.append('FAIL: outer wrapper not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
