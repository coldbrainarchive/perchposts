#!/usr/bin/env python3
"""Patch v495 -> v496: Change remove system chirp emoji from 👢 to 💨."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v495.js'
dst = '_deploy/assets/index-DUcNPOLc-v496.js'

content = open(src, encoding='utf-8').read()

OLD = '`👢 ${_wpRemP.u} was removed from the huddle`'
NEW = '`💨 ${_wpRemP.u} was removed from the huddle`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: emoji 👢 → 💨')
else:
    print('FAIL'); sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
