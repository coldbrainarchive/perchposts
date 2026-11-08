#!/usr/bin/env python3
"""Patch v166 -> v167: show post body text on link posts, same style as normal posts."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v166.js'
dst = '_deploy/assets/index-DUcNPOLc-v167.js'

content = open(src, encoding='utf-8').read()
errors = []

# For link posts the body text `f` is never rendered — only the title and the
# link preview card show.  Add `f` between them using the same style as Pr uses
# for regular post body text.
OLD = (
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,className:`feed-post-title`,'
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:6},'
    'children:e.title}),(0,L.jsx)(Fr,{attachment:p,postId:e.id})'
)
NEW = (
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,className:`feed-post-title`,'
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:6},'
    'children:e.title}),'
    'f&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:14,lineHeight:1.55,'
    'whiteSpace:`pre-wrap`,marginBottom:8},'
    'children:f.length>200?f.slice(0,200)+`…`:f}),'
    '(0,L.jsx)(Fr,{attachment:p,postId:e.id})'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: body text added to link post render')
else:
    errors.append('FAIL: link post fragment not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
