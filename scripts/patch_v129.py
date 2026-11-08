#!/usr/bin/env python3
"""Patch v128 -> v129: tap anywhere on link preview panel to close it."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v128.js'
dst = '_deploy/assets/index-DUcNPOLc-v129.js'

content = open(src, encoding='utf-8').read()
errors = []

# Change inner panel from stopPropagation to close on tap.
# Links/buttons inside already stop propagation or handle navigation themselves.
OLD = 'borderRadius:`20px 20px 0 0`,maxHeight:`80vh`,display:`flex`,flexDirection:`column`},onClick:e=>e.stopPropagation()'
NEW = 'borderRadius:`20px 20px 0 0`,maxHeight:`80vh`,display:`flex`,flexDirection:`column`},onClick:e=>{if(e.target.tagName!==`A`&&e.target.tagName!==`BUTTON`&&e.target.tagName!==`IMG`)l()}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: link preview panel closes on tap anywhere except links/buttons/images')
else:
    errors.append('FAIL: panel onClick pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
