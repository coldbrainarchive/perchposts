#!/usr/bin/env python3
"""Patch v149 -> v150: fix centring by targeting the base .user-pill CSS directly."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v149.js'
dst = '_deploy/assets/index-DUcNPOLc-v150.js'

content = open(src, encoding='utf-8').read()
errors = []

# When inline-flex is blockified as a flex item it can fill its container width,
# leaving the badge left-aligned.  Fix: add justify-content:center to the base
# .user-pill rule and equalise padding so the badge is always centred.
# justify-content:center has no visual effect on full pills (badge+text)
# because those pills shrink to fit content anyway.
OLD_PILL_CSS = (
    'display: inline-flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        height: 22px;\n'
    '        padding: 0 9px 0 6px;\n'
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

if OLD_PILL_CSS in content:
    content = content.replace(OLD_PILL_CSS, NEW_PILL_CSS, 1)
    print('OK: base .user-pill gets justify-content:center + equal padding')
else:
    errors.append('FAIL: .user-pill CSS block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
