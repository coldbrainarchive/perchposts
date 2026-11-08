#!/usr/bin/env python3
"""Patch v89 -> v90:
- Copy button: show ✓ confirmation for 1.5s after copying
- Post card with link attachment: show post title above the link preview
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v89.js'
dst = '_deploy/assets/index-DUcNPOLc-v90.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Copy button: add confirmation flash ────────────────────────────────────
OLD_COPY = (
    'onClick:function(){try{navigator.clipboard.writeText(r)}catch(err){}}'
)
NEW_COPY = (
    'onClick:function(ev){'
    'try{'
    'navigator.clipboard.writeText(r);'
    'var b=ev.currentTarget;'
    'b.textContent="✓";'
    'b.style.color="#22c55e";'
    'setTimeout(function(){b.textContent="\U0001f4cb";b.style.color="#64748b"},1500)'
    '}catch(err){}}'
)

if OLD_COPY in content:
    content = content.replace(OLD_COPY, NEW_COPY, 1)
    print('OK: copy button - added confirmation flash')
else:
    errors.append('FAIL: copy button onClick not found')

# ── 2. Post card: show title above link/video attachment ──────────────────────
# Current: p&&p.type!==`image`?(0,L.jsx)(Fr,{attachment:p,postId:e.id}):...
# Change to: wrap in Fragment, show e.title as a link before Fr
OLD_FR = (
    'p&&p.type!==`image`?(0,L.jsx)(Fr,{attachment:p,postId:e.id})'
)
NEW_FR = (
    'p&&p.type!==`image`?'
    '(0,L.jsxs)(L.Fragment,{children:['
    'e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:6},children:(0,L.jsx)(`div`,{style:{color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35},children:e.title})}),'
    '(0,L.jsx)(Fr,{attachment:p,postId:e.id})'
    ']})'
)

if OLD_FR in content:
    count = content.count(OLD_FR)
    content = content.replace(OLD_FR, NEW_FR)
    print(f'OK: post card - added title above link attachment ({count} occurrence(s))')
else:
    errors.append('FAIL: post card Fr pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
