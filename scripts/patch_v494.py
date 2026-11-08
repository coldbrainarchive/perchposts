#!/usr/bin/env python3
"""Patch v493 -> v494: Change the actual sidebar panel background to #0b0f12.
Target the specific occurrence with min(420px, 100vw) context."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v493.js'
dst = '_deploy/assets/index-DUcNPOLc-v494.js'

content = open(src, encoding='utf-8').read()

OLD = ('width:`min(420px, 100vw)`,background:`linear-gradient(180deg, #1b1d24 0%, #14161c 100%)`,borderLeft:`1px solid #2e303a`')
NEW = ('width:`min(420px, 100vw)`,background:`#0b0f12`,borderLeft:`1px solid #2e303a`')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: sidebar panel → #0b0f12')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
