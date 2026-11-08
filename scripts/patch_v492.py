#!/usr/bin/env python3
"""Patch v490 -> v492: Only change the sign-in panel background to #0b0f12.
The sign-in panel is the one with onClick:e=>e.stopPropagation()."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v490.js'
dst = '_deploy/assets/index-DUcNPOLc-v492.js'

content = open(src, encoding='utf-8').read()

OLD = ('background:`#1a1d27`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`,'
       'display:`flex`,flexDirection:`column`},onClick:e=>e.stopPropagation()')
NEW = ('background:`#0b0f12`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`,'
       'display:`flex`,flexDirection:`column`},onClick:e=>e.stopPropagation()')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: sign-in panel → #0b0f12')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
