#!/usr/bin/env python3
"""Patch v596 -> v597: Bird button keeps action panel open (remove y(!1) call)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v596.js'
dst = '_deploy/assets/index-DUcNPOLc-v597.js'

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

patch(
    'onClick:()=>{y(!1);fetch(`${R}/user-stats?username=${encodeURIComponent(e.username)}`).then(r=>r.json()).then(d=>{_setBirdStats(d);_setBirdOpen(!0);}).catch(()=>_setBirdOpen(!0));},children:`Bird`',
    'onClick:()=>{fetch(`${R}/user-stats?username=${encodeURIComponent(e.username)}`).then(r=>r.json()).then(d=>{_setBirdStats(d);_setBirdOpen(!0);}).catch(()=>_setBirdOpen(!0));},children:`Bird`',
    'Bird button keeps action panel open'
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
