#!/usr/bin/env python3
"""Patch v496 -> v497: Remove 🗑 emoji from Delete buttons."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v496.js'
dst = '_deploy/assets/index-DUcNPOLc-v497.js'

content = open(src, encoding='utf-8').read()

OLD = '[(0,L.jsx)(`span`,{children:`🗑`}),(0,L.jsx)(`span`,{children:`Delete`})]'
NEW = '`Delete`'

n = content.count(OLD)
if n > 0:
    content = content.replace(OLD, NEW)
    print(f'OK: 🗑 removed from {n} Delete button(s)')
else:
    print('FAIL'); sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
