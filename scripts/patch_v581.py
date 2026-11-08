#!/usr/bin/env python3
"""Patch v578 -> v581: Restructure ChatMessage so everything is inside the bubble.
New order inside bubble: text → action sheet → reactions → attachment.
Removes action sheet and reactions from outside the bubble."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v578.js'
dst = '_deploy/assets/index-DUcNPOLc-v581.js'

content = open(src, encoding='utf-8').read()

# ── Extract exact live strings ──
idx_as = content.find('v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`')
end_as = content.find('),b&&', idx_as) + 1
ACTION_SHEET = content[idx_as:end_as]   # v&&(0,L.jsxs)(...Delete...})])

idx_rx = content.find('ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`')
end_rx = content.find('}),v&&', idx_rx) + 2
REACTIONS = content[idx_rx:end_rx]      # ee.length>0&&(0,L.jsx)(...})

TEXT_IIFE_OLD = (
    '(({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment,{children:'
    '[_ct&&(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}),'
    '_ca&&(0,L.jsx)(`div`,{style:{marginTop:_ct?6:0},onClick:_ev=>_ev.stopPropagation(),'
    'children:(0,L.jsx)(Fr,{attachment:_ca})})]}))( Mr(e.content))'
)

TEXT_IIFE_NEW = (
    '(({text:_ct})=>_ct?(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}):null)'
    '(Mr(e.content))'
)

ATTACH_IIFE = (
    '(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:6},'
    'children:(0,L.jsx)(Fr,{attachment:_ca})}):null)(Mr(e.content))'
)

# OLD: IIFE inside bubble] + ,reactions,action_sheet,
OLD = (
    TEXT_IIFE_OLD +
    ']})'  +          # closes bubble children [] + bubble jsx
    ',' + REACTIONS +
    ',' + ACTION_SHEET +
    ','               # trailing comma before b&&emoji
)

# NEW: text+action_sheet+reactions+attachment inside bubble] + ,
NEW = (
    TEXT_IIFE_NEW +
    ',' + ACTION_SHEET +
    ',' + REACTIONS +
    ',' + ATTACH_IIFE +
    ']})' +           # closes bubble children [] + bubble jsx (same as OLD's ]})
    ','               # trailing comma before b&&emoji
)

errors = []
n = content.count(OLD)
if n == 0:
    errors.append('FAIL: OLD sequence not found')
elif n > 1:
    errors.append(f'FAIL: {n} matches')
else:
    content = content.replace(OLD, NEW)
    print('OK: restructured bubble contents')

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
