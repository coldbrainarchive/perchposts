#!/usr/bin/env python3
"""Patch v604 -> v606:
Simplify scroll-to-bottom: fire once at 200ms on initial load only.
No triple-firing = no jumping. After user sends a comment, still scrolls immediately.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v604.js'
dst = '_deploy/assets/index-DUcNPOLc-v606.js'

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

# Replace triple-fire scroll with single 200ms delayed scroll on initial load
patch(
    'if(!_isd.current){_isd.current=!0;e.scrollTop=e.scrollHeight;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},400);setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},1200);return;}if(O.current){e.scrollTop=e.scrollHeight;}',
    'if(!_isd.current){_isd.current=!0;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},200);return;}if(O.current){e.scrollTop=e.scrollHeight;}',
    'single 200ms scroll on initial load only'
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
