#!/usr/bin/env python3
"""Patch v119 -> v120: move cage notice to beside the board tag, brown text, no box."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v119.js'
dst = '_deploy/assets/index-DUcNPOLc-v120.js'

content = open(src, encoding='utf-8').read()
errors = []

MSG = "You’re caged — you can only post and comment in \U0001fab9 The Cage"

# 1. Remove the yellow notice box (injected before feed-post-main)
OLD_BOX = (
    'p&&(0,L.jsx)(`div`,{style:{background:`rgba(251,191,36,0.08)`,border:`1px solid rgba(251,191,36,0.25)`,'
    'borderRadius:10,padding:`8px 12px`,margin:`0 0 10px`,fontSize:12,color:`#fbbf24`,textAlign:`center`},'
    f'children:`{MSG}`}})'
)
if OLD_BOX in content:
    content = content.replace(OLD_BOX, '', 1)
    print('OK: removed yellow notice box')
else:
    errors.append('FAIL: yellow notice box not found')

# 2. Add inline brown text beside the board tag pill
OLD_BTN = 'cursor:p?`default`:`pointer`},children:(0,L.jsx)(Ar,{boardName:oe.name,small:!0})})'
NEW_BTN = (
    'cursor:p?`default`:`pointer`},children:(0,L.jsx)(Ar,{boardName:oe.name,small:!0})})'
    ',p&&(0,L.jsx)(`span`,{style:{fontSize:11,color:`#92400e`,fontWeight:500,marginLeft:4},'
    f'children:`{MSG}`}})'
)
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: brown cage text added beside board tag')
else:
    errors.append('FAIL: board button pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
