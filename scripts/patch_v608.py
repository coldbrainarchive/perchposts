#!/usr/bin/env python3
"""Patch v607 -> v608:
Fix sort toggle buttons — with column-reverse the conditional sort logic breaks.
Make Oldest/Newest buttons pure scroll shortcuts that always jump to the respective end.
- Oldest: always scrolls to top (scrollHeight) to show oldest comments
- Newest: always scrolls to bottom (0) to show newest comments
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v607.js'
dst = '_deploy/assets/index-DUcNPOLc-v608.js'

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

# Oldest button: remove if(b) condition, always scroll to top
patch(
    'onClick:()=>{if(b){let e=D.current;e&&e.scrollTo({top:e.scrollHeight,behavior:`smooth`});x(!1);}}',
    'onClick:()=>{let e=D.current;e&&e.scrollTo({top:e.scrollHeight,behavior:`smooth`});}',
    'oldest btn always scrolls to top'
)

# Newest button: remove if(!b) condition, always scroll to bottom
patch(
    'onClick:()=>{if(!b){let e=D.current;e&&e.scrollTo({top:0,behavior:`smooth`});x(!0);}}',
    'onClick:()=>{let e=D.current;e&&e.scrollTo({top:0,behavior:`smooth`});}',
    'newest btn always scrolls to bottom'
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
