#!/usr/bin/env python3
"""Patch v151 -> v152: switch nav button to inline-flex so it hugs the pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v151.js'
dst = '_deploy/assets/index-DUcNPOLc-v152.js'

content = open(src, encoding='utf-8').read()
errors = []

# display:flex on the button is block-level — it fills its container and the
# pill left-aligns inside the extra space. Switching to inline-flex makes the
# button hug its content so there is no extra space to misalign within.
OLD_BTN = (
    'nav-user-pill`,style:{background:`none`,border:`none`,'
    'padding:0,cursor:`pointer`,display:`flex`,'
    'justifyContent:`center`,alignItems:`center`}'
)
NEW_BTN = (
    'nav-user-pill`,style:{background:`none`,border:`none`,'
    'padding:0,cursor:`pointer`,display:`inline-flex`,'
    'justifyContent:`center`,alignItems:`center`}'
)

if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: nav button switched to inline-flex')
else:
    errors.append('FAIL: nav-user-pill button style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
