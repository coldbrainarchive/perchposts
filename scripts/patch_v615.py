#!/usr/bin/env python3
"""Patch v614 -> v615:
Attach button on new post page: show spinning SVG while uploading (ne=true)
instead of the plain '…' text. Same spinner style as the comment attach button.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v614.js'
dst = '_deploy/assets/index-DUcNPOLc-v615.js'

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
    'children:ne?`…`:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`span`,{style:{display:`inline-block`,transform:`scaleX(-1)`},children:`📎`}),` Attach`]})',
    'children:ne?(0,L.jsx)(`svg`,{width:14,height:14,viewBox:`0 0 16 16`,fill:`none`,style:{animation:`_caSpin 0.8s linear infinite`,verticalAlign:`middle`},children:(0,L.jsx)(`circle`,{cx:8,cy:8,r:6,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,strokeDasharray:`28`,strokeDashoffset:`10`})}):(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`span`,{style:{display:`inline-block`,transform:`scaleX(-1)`},children:`📎`}),` Attach`]})',
    'spinner on Attach button while uploading'
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
