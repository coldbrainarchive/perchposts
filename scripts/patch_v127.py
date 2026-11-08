#!/usr/bin/env python3
"""Patch v126 -> v127: smaller centered count in notification pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v126.js'
dst = '_deploy/assets/index-DUcNPOLc-v127.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'background:`#ef4444`,borderColor:`#ef4444`,color:`#ffffff`,fontWeight:800,fontSize:14,minWidth:28,justifyContent:`center`'
NEW = 'background:`#ef4444`,borderColor:`#ef4444`,color:`#ffffff`,fontWeight:700,fontSize:11,minWidth:28,display:`flex`,alignItems:`center`,justifyContent:`center`,textAlign:`center`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: count smaller and centered')
else:
    errors.append('FAIL: pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
