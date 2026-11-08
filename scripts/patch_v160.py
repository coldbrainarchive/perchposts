#!/usr/bin/env python3
"""Patch v159 -> v160: fix link preview/post title alignment to match normal posts."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v159.js'
dst = '_deploy/assets/index-DUcNPOLc-v160.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Link preview card content column: justifyContent center floats the title
#    to the vertical middle when there's no description. Change to flex-start
#    so the title sits at the top like a normal post title.
OLD_NR_COL = (
    'style:{flex:1,padding:`16px 14px`,minWidth:0,display:`flex`,'
    'flexDirection:`column`,justifyContent:`center`,textAlign:`left`}'
)
NEW_NR_COL = (
    'style:{flex:1,padding:`16px 14px`,minWidth:0,display:`flex`,'
    'flexDirection:`column`,justifyContent:`flex-start`,textAlign:`left`}'
)
if OLD_NR_COL in content:
    content = content.replace(OLD_NR_COL, NEW_NR_COL)  # both Nr and Pr share this pattern
    print(f'OK: link preview content column set to flex-start')
else:
    errors.append('FAIL: Nr content column not found')

# 2. Link post title (e.title rendered above Fr/Nr in the feed card): replace
#    the small inline-styled div with the feed-post-title class so it looks
#    identical to a regular post title.
OLD_LINK_TITLE = (
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,'
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:6},'
    'children:(0,L.jsx)(`div`,{style:{color:`#f1f5f9`,fontWeight:700,'
    'fontSize:16,lineHeight:1.35},children:e.title})})'
)
NEW_LINK_TITLE = (
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,'
    'className:`feed-post-title`,'
    'style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:6},'
    'children:e.title})'
)
if OLD_LINK_TITLE in content:
    content = content.replace(OLD_LINK_TITLE, NEW_LINK_TITLE, 1)
    print('OK: link post title uses feed-post-title class')
else:
    errors.append('FAIL: link post title not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
