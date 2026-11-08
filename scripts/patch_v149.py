#!/usr/bin/env python3
"""Patch v148 -> v149: centre nav pill via inline style on the button itself."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v148.js'
dst = '_deploy/assets/index-DUcNPOLc-v149.js'

content = open(src, encoding='utf-8').read()
errors = []

# The outer display:flex button fills its container width, so the inner pill
# left-aligns. CSS overrides keep losing. Fix it directly in the inline style.
OLD_BTN = (
    'nav-user-pill`,style:{background:`none`,border:`none`,'
    'padding:0,cursor:`pointer`,display:`flex`}'
)
NEW_BTN = (
    'nav-user-pill`,style:{background:`none`,border:`none`,'
    'padding:0,cursor:`pointer`,display:`flex`,'
    'justifyContent:`center`,alignItems:`center`}'
)

if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: nav button inline style centred')
else:
    errors.append('FAIL: nav-user-pill button style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
