#!/usr/bin/env python3
"""Patch v361 -> v362: make POST/HUDDLE toggle same height as small board/user pills (22px)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v361.js'
dst = '_deploy/assets/index-DUcNPOLc-v362.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '`sort-toggle`,style:{width:`fit-content`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`HUDDLE`})'
    ']}'
)
NEW = (
    '`sort-toggle`,style:{width:`fit-content`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'style:{height:22,padding:`0 8px`,fontSize:10},'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'style:{height:22,padding:`0 8px`,fontSize:10},'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`HUDDLE`})'
    ']}'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: toggle buttons sized to 22px to match pills')
else:
    errors.append('FAIL: toggle not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
