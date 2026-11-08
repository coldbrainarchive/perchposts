#!/usr/bin/env python3
"""Patch v150 -> v151: fix pill width so it wraps content, then centre in button."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v150.js'
dst = '_deploy/assets/index-DUcNPOLc-v151.js'

content = open(src, encoding='utf-8').read()
errors = []

# The pill (inline-flex) gets blockified as a flex item and stretches to the
# button width. justify-content:center then centres badge in the WIDE box, not
# visually in the pill. Fix: give the pill width:max-content so it only wraps
# its actual content, and revert justify-content to flex-start. The button's
# justify-content:center (already in inline style) then centres the narrow pill.
OLD_PILL_CSS = (
    'display: inline-flex;\n'
    '        align-items: center;\n'
    '        justify-content: center;\n'
    '        gap: 6px;\n'
    '        height: 22px;\n'
    '        padding: 0 8px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid;\n'
    '        font-size: 12px;\n'
    '        font-weight: 700;\n'
    '        line-height: 1;\n'
    '        white-space: nowrap;\n'
    '        flex-shrink: 0;\n'
    '        box-sizing: border-box;'
)
NEW_PILL_CSS = (
    'display: inline-flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        height: 22px;\n'
    '        width: max-content;\n'
    '        padding: 0 8px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid;\n'
    '        font-size: 12px;\n'
    '        font-weight: 700;\n'
    '        line-height: 1;\n'
    '        white-space: nowrap;\n'
    '        flex-shrink: 0;\n'
    '        box-sizing: border-box;'
)

if OLD_PILL_CSS in content:
    content = content.replace(OLD_PILL_CSS, NEW_PILL_CSS, 1)
    print('OK: pill gets width:max-content, justify-content reverted to default')
else:
    errors.append('FAIL: .user-pill CSS block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
