#!/usr/bin/env python3
"""Patch v539 -> v540: Show sign-in placeholder on Huddles board when logged out."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v539.js'
dst = '_deploy/assets/index-DUcNPOLc-v540.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'className:`home-feed`,children:[b.slice(0,o).map(e=>'
NEW = ('className:`home-feed`,children:['
       '_isHuddleBoard&&!localStorage.getItem(`auth_token`)&&(0,L.jsxs)(`div`,{'
       'style:{display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,'
       'padding:`64px 24px`,textAlign:`center`,gap:12},'
       'children:['
       '(0,L.jsx)(`div`,{style:{fontSize:48,marginBottom:4},children:`👥`}),'
       '(0,L.jsx)(`div`,{style:{fontSize:17,fontWeight:700,color:`#f1f5f9`},children:`Sign in to start a huddle`}),'
       '(0,L.jsx)(`div`,{style:{fontSize:13,color:`#64748b`,marginTop:2},children:`Huddles are private spaces — sign in to create or join one`})'
       ']}),'
       'b.slice(0,o).map(e=>')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: sign-in placeholder added to Huddles board')
else:
    errors.append('FAIL: home-feed children not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
