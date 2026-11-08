#!/usr/bin/env python3
"""Patch v127 -> v128: notification pill matches New Post pill size using app-chip class."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v127.js'
dst = '_deploy/assets/index-DUcNPOLc-v128.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'className:`user-pill`,style:{background:`#ef4444`,borderColor:`#ef4444`,color:`#ffffff`,fontWeight:700,fontSize:11,minWidth:28,display:`flex`,alignItems:`center`,justifyContent:`center`,textAlign:`center`}'
NEW = 'className:`app-chip`,style:{background:`#ef4444`,borderColor:`#ef4444`,color:`#ffffff`}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: notification pill now uses app-chip sizing')
else:
    errors.append('FAIL: notification pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
