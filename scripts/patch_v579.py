#!/usr/bin/env python3
"""Patch v578 -> v579:
1. Tapping comment name/meta row also opens actions
2. Move attachment outside the bubble (between bubble and reactions)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v578.js'
dst = '_deploy/assets/index-DUcNPOLc-v579.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# ── 1. Add onClick to chat-msg-meta so tapping name opens actions ──
patch(
    'className:`chat-msg-meta`,style:{background:e.is_admin===true?`#ffffff`:h}',
    'className:`chat-msg-meta`,onClick:()=>!p&&y(_s=>!_s),style:{cursor:`pointer`,background:e.is_admin===true?`#ffffff`:h}',
    'name row tap opens actions'
)

# ── 2. Remove attachment from inside bubble + render it between bubble and reactions ──
patch(
    '(({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment,{children:[_ct&&(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}),_ca&&(0,L.jsx)(`div`,{style:{marginTop:_ct?6:0},onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca})})]}))( Mr(e.content))]}),ee.length>0&&',
    '(({text:_ct})=>_ct?(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}):null)(Mr(e.content))]})' +',(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:6},children:(0,L.jsx)(Fr,{attachment:_ca})}):null)(Mr(e.content)),ee.length>0&&',
    'move attachment outside bubble'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
