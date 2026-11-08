#!/usr/bin/env python3
"""Patch v333 -> v334: defer initial scroll to bottom with double-rAF so DOM is fully painted."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v333.js'
dst = '_deploy/assets/index-DUcNPOLc-v334.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the scroll logic with double-rAF so scrollHeight is final when we read it
OLD_SCROLL = (
    'if(A.current||u.length===0)return;'
    'A.current=!0;let e=D.current;'
    'if(e){e.scrollTop=e.scrollHeight;}'
    'window.scrollTo({top:document.body.scrollHeight})'
)
NEW_SCROLL = (
    'if(A.current||u.length===0)return;'
    'A.current=!0;'
    'requestAnimationFrame(()=>requestAnimationFrame(()=>{'
    'let e=D.current;'
    'if(e)e.scrollTop=e.scrollHeight;'
    'window.scrollTo(0,document.body.scrollHeight);'
    '}))'
)
if OLD_SCROLL in content:
    content = content.replace(OLD_SCROLL, NEW_SCROLL, 1)
    print('OK: initial scroll deferred with double-rAF')
else:
    errors.append('FAIL: scroll logic not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
