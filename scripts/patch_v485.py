#!/usr/bin/env python3
"""Patch v474 -> v485: Make the notification panel background black."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v485.js'

content = open(src, encoding='utf-8').read()

OLD = 'position:`relative`,background:`#1a1d27`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`'
NEW = 'position:`relative`,background:`#000000`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: panel background → black')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
