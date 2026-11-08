#!/usr/bin/env python3
"""Patch v492 -> v493: Change the desktop sidebar (sign-in container) from
linear-gradient to #0b0f12 to match the nav header black."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v492.js'
dst = '_deploy/assets/index-DUcNPOLc-v493.js'

content = open(src, encoding='utf-8').read()

OLD = 'background:`linear-gradient(180deg, #1b1d24 0%, #14161c 100%)`'
NEW = 'background:`#0b0f12`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: sign-in panel sidebar gradient → #0b0f12')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
