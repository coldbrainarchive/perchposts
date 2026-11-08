#!/usr/bin/env python3
"""Patch v489 -> v490: Match notification panel header to nav bar color #0b0f12."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v489.js'
dst = '_deploy/assets/index-DUcNPOLc-v490.js'

content = open(src, encoding='utf-8').read()

OLD = 'position:`relative`,background:`#000000`}'
NEW = 'position:`relative`,background:`#0b0f12`}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: header #000000 → #0b0f12 (matches nav bar)')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
