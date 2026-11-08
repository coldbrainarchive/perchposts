#!/usr/bin/env python3
"""Patch v168 -> v169: explicitly left-align link post title."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v168.js'
dst = '_deploy/assets/index-DUcNPOLc-v169.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,'
    'color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35},'
    'children:e.title}'
)
NEW = (
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,'
    'color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:`left`},'
    'children:e.title}'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: textAlign:left added to link post title')
else:
    errors.append('FAIL: link post title style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
