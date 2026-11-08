#!/usr/bin/env python3
"""Patch v618 -> v620: Increase postcard thumbnail width from 100px to 140px."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v618.js'
dst = '_deploy/assets/index-DUcNPOLc-v620.js'

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

# Use unique context: Pr's image div comes after "View Huddle →":"View Post →"
patch(
    'View Huddle →`:`View Post →`})]}),r&&(0,L.jsxs)(`div`,{style:{width:100,flexShrink:0,position:`relative`,overflow:`hidden`}',
    'View Huddle →`:`View Post →`})]}),r&&(0,L.jsxs)(`div`,{style:{width:140,flexShrink:0,position:`relative`,overflow:`hidden`}',
    'postcard thumbnail width 100 -> 140'
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
