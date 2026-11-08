#!/usr/bin/env python3
"""Patch v120 -> v121: remove duplicate Caged badge, update cage text."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v120.js'
dst = '_deploy/assets/index-DUcNPOLc-v121.js'

content = open(src, encoding='utf-8').read()
errors = []

# Unicode curly apostrophe and em dash used in the bundle
OLD_MSG = "You’re caged — you can only post and comment in \U0001fab9 The Cage"
NEW_MSG = "You’re Caged! You can only post and comment in \U0001fab9 The Cage"

# 1. Remove the duplicate 🪹 Caged badge in new post form header
OLD_BADGE = ',p&&(0,L.jsx)(`span`,{style:{fontSize:11,fontWeight:700,color:`#fbbf24`},children:`\U0001fab9 Caged`})'
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, '', 1)
    print('OK: removed duplicate Caged badge')
else:
    errors.append('FAIL: Caged badge not found')

# 2. Update all cage messages
count = content.count(OLD_MSG)
if count > 0:
    content = content.replace(OLD_MSG, NEW_MSG)
    print(f'OK: updated {count} cage message(s)')
else:
    errors.append(f'FAIL: cage message not found (looking for: {repr(OLD_MSG[:40])})')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
