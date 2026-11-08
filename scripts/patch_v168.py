#!/usr/bin/env python3
"""Patch v167 -> v168: remove body text from link posts, match title style to Pr."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v167.js'
dst = '_deploy/assets/index-DUcNPOLc-v168.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,className:`feed-post-title`,'
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:6},'
    'children:e.title}),'
    'f&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:14,lineHeight:1.55,'
    'whiteSpace:`pre-wrap`,marginBottom:8},'
    'children:f.length>200?f.slice(0,200)+`…`:f}),'
    '(0,L.jsx)(Fr,{attachment:p,postId:e.id})'
)
# Match Pr's title style exactly: 16px bold #f1f5f9 — no body text, no CSS class
NEW = (
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,'
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,'
    'color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35},'
    'children:e.title}),'
    '(0,L.jsx)(Fr,{attachment:p,postId:e.id})'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: body text removed, title style matches Pr')
else:
    errors.append('FAIL: link post title+body block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
