#!/usr/bin/env python3
"""Patch v608 -> v609:
Replace scrollTo({behavior:'smooth'}) with direct scrollTop assignment on sort buttons.
scrollTo with smooth behavior is unreliable on iOS Safari — direct scrollTop works everywhere.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v608.js'
dst = '_deploy/assets/index-DUcNPOLc-v609.js'

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

# Oldest button: scrollTo -> direct scrollTop
patch(
    'onClick:()=>{let e=D.current;e&&e.scrollTo({top:e.scrollHeight,behavior:`smooth`});}',
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=e.scrollHeight;}',
    'oldest btn direct scrollTop'
)

# Newest button: scrollTo -> direct scrollTop
patch(
    'onClick:()=>{let e=D.current;e&&e.scrollTo({top:0,behavior:`smooth`});}',
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=0;}',
    'newest btn direct scrollTop'
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
