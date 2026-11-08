#!/usr/bin/env python3
"""Patch v510 -> v511: Show deleted/archived banner on post page for mods."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v510.js'
dst = '_deploy/assets/index-DUcNPOLc-v511.js'

content = open(src, encoding='utf-8').read()
errors = []

# Insert a deleted/archived banner above the post title
OLD = ('children:[c.title&&(0,L.jsx)(`h2`,{style:{margin:e?`0 0 8px`:`0`,'
       'fontSize:18,fontWeight:800,color:`#f8fafc`,lineHeight:1.3,textAlign:`left`},'
       'children:c.title}),')
NEW = ('children:[c.deleted&&(0,L.jsx)(`div`,{style:{marginBottom:10,padding:`6px 12px`,'
       'borderRadius:8,background:`rgba(239,68,68,0.12)`,border:`1px solid rgba(239,68,68,0.3)`,'
       'color:`#f87171`,fontSize:12,fontWeight:700,letterSpacing:`0.04em`},'
       'children:`⚠ DELETED — visible to mods only`}),'
       'c.archived&&!c.deleted&&(0,L.jsx)(`div`,{style:{marginBottom:10,padding:`6px 12px`,'
       'borderRadius:8,background:`rgba(251,191,36,0.10)`,border:`1px solid rgba(251,191,36,0.3)`,'
       'color:`#fbbf24`,fontSize:12,fontWeight:700,letterSpacing:`0.04em`},'
       'children:`⚠ ARCHIVED — visible to mods only`}),'
       'c.title&&(0,L.jsx)(`h2`,{style:{margin:e?`0 0 8px`:`0`,'
       'fontSize:18,fontWeight:800,color:`#f8fafc`,lineHeight:1.3,textAlign:`left`},'
       'children:c.title}),')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: deleted/archived banner added to post page')
else:
    errors.append('FAIL: post title location not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
