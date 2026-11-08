#!/usr/bin/env python3
"""Patch v609 -> v611:
Fix sort toggle buttons using scrollIntoView on actual child elements.
scrollTop on column-reverse containers has a 0 scroll range in many browsers.
scrollIntoView works on the element directly regardless of scroll container behavior.
Also restores x(!1)/x(!0) so the active button highlight animates correctly.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v609.js'
dst = '_deploy/assets/index-DUcNPOLc-v611.js'

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

# Oldest: scrollIntoView on lastElementChild (oldest = last in DOM with column-reverse)
# restore x(!1) so the active state highlight toggles back
patch(
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=e.scrollHeight;},children:`Oldest`',
    'onClick:()=>{let e=D.current;if(e&&e.lastElementChild){e.lastElementChild.scrollIntoView();x(!1);}},children:`Oldest`',
    'oldest btn scrollIntoView lastElementChild'
)

# Newest: scrollIntoView on firstElementChild (newest = first in DOM with column-reverse)
# restore x(!0) so the active state highlight toggles
patch(
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=0;},children:`Newest`',
    'onClick:()=>{let e=D.current;if(e&&e.firstElementChild){e.firstElementChild.scrollIntoView();x(!0);}},children:`Newest`',
    'newest btn scrollIntoView firstElementChild'
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
