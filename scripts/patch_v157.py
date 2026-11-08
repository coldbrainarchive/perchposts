#!/usr/bin/env python3
"""Patch v156 -> v157: revert all pill-centering changes back to v146 baseline."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v156.js'
dst = '_deploy/assets/index-DUcNPOLc-v157.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Revert Xn pill inline style — remove justifyContent + padding additions
OLD_XN = 'cursor:r?`pointer`:`default`,justifyContent:`center`,padding:`0 8px`}'
NEW_XN = 'cursor:r?`pointer`:`default`}'
if OLD_XN in content:
    content = content.replace(OLD_XN, NEW_XN, 1)
    print('OK: Xn inline style reverted')
else:
    errors.append('FAIL: Xn inline style not found')

# 2. Revert badge inline style — remove margin:auto
OLD_BADGE_INLINE = (
    'width:`1.1em`,height:`1.1em`,lineHeight:1,verticalAlign:`middle`,margin:`auto`}'
)
NEW_BADGE_INLINE = (
    'width:`1.1em`,height:`1.1em`,lineHeight:1,verticalAlign:`middle`}'
)
if OLD_BADGE_INLINE in content:
    content = content.replace(OLD_BADGE_INLINE, NEW_BADGE_INLINE, 1)
    print('OK: badge inline style reverted')
else:
    errors.append('FAIL: badge inline style not found')

# 3. Revert button back to display:flex (no justifyContent/alignItems)
OLD_BTN = (
    'nav-user-pill`,style:{background:`none`,border:`none`,'
    'padding:0,cursor:`pointer`,display:`inline-flex`,'
    'justifyContent:`center`,alignItems:`center`}'
)
NEW_BTN = (
    'nav-user-pill`,style:{background:`none`,border:`none`,'
    'padding:0,cursor:`pointer`,display:`flex`}'
)
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: button reverted to display:flex')
else:
    errors.append('FAIL: button style not found')

# 4. Revert badge CSS — remove margin:auto
OLD_BADGE_CSS = (
    'user-pill-badge {\n'
    '        font-size: 12px;\n'
    '        line-height: 1;\n'
    '        margin: auto;\n'
    '      }'
)
NEW_BADGE_CSS = (
    'user-pill-badge {\n'
    '        font-size: 12px;\n'
    '        line-height: 1;\n'
    '      }'
)
if OLD_BADGE_CSS in content:
    content = content.replace(OLD_BADGE_CSS, NEW_BADGE_CSS, 1)
    print('OK: badge CSS reverted')
else:
    errors.append('FAIL: badge CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
