#!/usr/bin/env python3
"""Patch v145 -> v146: remove username truncation + increase badge/text gap."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v145.js'
dst = '_deploy/assets/index-DUcNPOLc-v146.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove truncation from user-pill-name ─────────────────────────────────
OLD_NAME_CSS = (
    'user-pill-name {\n'
    '        max-width: 160px;\n'
    '        overflow: hidden;\n'
    '        text-overflow: ellipsis;\n'
    '        white-space: nowrap;\n'
    '      }'
)
NEW_NAME_CSS = (
    'user-pill-name {\n'
    '        white-space: nowrap;\n'
    '      }'
)

if OLD_NAME_CSS in content:
    content = content.replace(OLD_NAME_CSS, NEW_NAME_CSS, 1)
    print('OK: username truncation removed')
else:
    errors.append('FAIL: user-pill-name CSS not found')

# ── 2. Increase gap between badge emoji and username text ─────────────────────
OLD_GAP = 'gap: 4px;\n        height: 22px;\n        padding: 0 9px 0 6px;'
NEW_GAP = 'gap: 6px;\n        height: 22px;\n        padding: 0 9px 0 6px;'

if OLD_GAP in content:
    content = content.replace(OLD_GAP, NEW_GAP, 1)
    print('OK: pill gap increased to 6px')
else:
    errors.append('FAIL: pill gap CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
