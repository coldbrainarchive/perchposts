#!/usr/bin/env python3
"""Patch v200 -> v201: use 🥚 as the bird generator placeholder (before tapping to generate)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v200.js'
dst = '_deploy/assets/index-DUcNPOLc-v201.js'

content = open(src, encoding='utf-8').read()
errors = []

# Only the absolute-positioned large emoji shown before the user taps to generate
OLD = '(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:40,lineHeight:1},children:`🐤`})'
NEW = '(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:40,lineHeight:1},children:`🥚`})'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: bird generator placeholder → 🥚')
else:
    errors.append('FAIL: placeholder span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
