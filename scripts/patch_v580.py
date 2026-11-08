#!/usr/bin/env python3
"""Patch v579 -> v580: Move action sheet to between bubble and attachment.
Two surgical patches: remove attachment from before reactions, re-insert it after the bird modal."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v579.js'
dst = '_deploy/assets/index-DUcNPOLc-v580.js'

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

ATTACH = '(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:6},children:(0,L.jsx)(Fr,{attachment:_ca})}):null)(Mr(e.content))'

# ── 1. Remove attachment from its current position (before reactions) ──
patch(
    ATTACH + ',ee.length>0&&',
    'ee.length>0&&',
    'remove attachment from before reactions'
)

# ── 2. Re-insert attachment after the bird modal (end of action-sheet block), before reactions ──
patch(
    'border:`1.5px solid #c084fc`},children:`See Posts`})]})]})]}):null,]}',
    'border:`1.5px solid #c084fc`},children:`See Posts`})]})]})]}):null,' + ATTACH + ',]}',
    'insert attachment after action-sheet block'
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
