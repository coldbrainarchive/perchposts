#!/usr/bin/env python3
"""Patch v102 -> v103: mod pill solid purple with black text."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v102.js'
dst = '_deploy/assets/index-DUcNPOLc-v103.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'style:{color:o?`#0a0a0a`:c,background:o?`#ffffff`:`${c}18`,borderColor:o?`#ffffff`:`${c}55`,cursor:r?`pointer`:`default`}'
NEW = 'style:{color:(o||s)?`#0a0a0a`:c,background:o?`#ffffff`:s?`#c084fc`:`${c}18`,borderColor:o?`#ffffff`:s?`#c084fc`:`${c}55`,cursor:r?`pointer`:`default`}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: mod pill now solid purple with black text')
else:
    errors.append('FAIL: Xn pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
