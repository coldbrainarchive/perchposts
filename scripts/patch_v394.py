#!/usr/bin/env python3
"""Patch v392 -> v394:
- Add Clear notifications header as a sibling BEFORE the scroll container
  (avoids structural change to children array that caused the bracket error)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v392.js'
dst = '_deploy/assets/index-DUcNPOLc-v394.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'c===`notifications`&&(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1,overflowY:`auto`},'
    'children:g?'
)
# Add header as sibling before the scroll container — no structural change to scroll div
HEADER = (
    'c===`notifications`&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,'
    'justifyContent:`space-between`,padding:`10px 16px 6px`,flexShrink:0,'
    'borderBottom:`1px solid rgba(255,255,255,0.06)`},'
    'children:[(0,L.jsx)(`span`,{style:{fontSize:13,fontWeight:700,color:`#94a3b8`},children:`Notifications`}),'
    'j.length>0&&(0,L.jsx)(`button`,{type:`button`,'
    'onClick:async()=>{const _un=localStorage.getItem(`_myUsername`)||null;'
    'const _au=JSON.parse(localStorage.getItem(`auth_user`)||`{}`);'
    'const _p=new URLSearchParams();if(_au.sub)_p.set(`mod_user_id`,_au.sub);if(_un)_p.set(`username`,_un);'
    'await fetch(`${R}/clear-notifications?${_p}`,{method:`POST`,headers:er()}).catch(()=>{});h([]);},'
    'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,cursor:`pointer`,padding:`2px 6px`,borderRadius:6},'
    'children:`Clear all`})]}),'
)
NEW = HEADER + OLD

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Clear all header added as sibling before scroll container')
else:
    errors.append('FAIL: notifications panel anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
