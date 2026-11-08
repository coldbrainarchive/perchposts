#!/usr/bin/env python3
"""Patch v578 -> v591: Attachment renders first in comment bubble, body text below."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v578.js'
dst = '_deploy/assets/index-DUcNPOLc-v591.js'

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

# Swap order: attachment first, text second
# marginTop on attachment becomes marginBottom (spacing below attachment, before text)
patch(
    '(({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment,{children:[_ct&&(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}),_ca&&(0,L.jsx)(`div`,{style:{marginTop:_ct?6:0},onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca})})]}))( Mr(e.content))',
    '(({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment,{children:[_ca&&(0,L.jsx)(`div`,{style:{marginBottom:_ct?8:0},onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca})}),_ct&&(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct})]}))( Mr(e.content))',
    'attachment first, text below'
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
