#!/usr/bin/env python3
"""Patch v336 -> v337: disable browser scroll restoration so refresh always lands at bottom."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v336.js'
dst = '_deploy/assets/index-DUcNPOLc-v337.js'

content = open(src, encoding='utf-8').read()
errors = []

# The browser restores scroll position on refresh, fighting our scroll-to-bottom.
# Fix: set history.scrollRestoration = 'manual' and use a timeout for reliability.
OLD_SCROLL = (
    'if(A.current||u.length===0)return;'
    'A.current=!0;'
    'requestAnimationFrame(()=>requestAnimationFrame(()=>{'
    'let e=D.current;'
    'if(e)e.scrollTop=e.scrollHeight;'
    'window.scrollTo(0,document.body.scrollHeight);'
    '}))'
)
NEW_SCROLL = (
    'if(A.current||u.length===0)return;'
    'A.current=!0;'
    'if(history.scrollRestoration)history.scrollRestoration=`manual`;'
    'requestAnimationFrame(()=>requestAnimationFrame(()=>{'
    'let e=D.current;'
    'if(e)e.scrollTop=e.scrollHeight;'
    'window.scrollTo(0,document.body.scrollHeight);'
    'setTimeout(()=>{if(e)e.scrollTop=e.scrollHeight;},100);'
    '}))'
)
if OLD_SCROLL in content:
    content = content.replace(OLD_SCROLL, NEW_SCROLL, 1)
    print('OK: scroll restoration disabled, added 100ms fallback scroll')
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
