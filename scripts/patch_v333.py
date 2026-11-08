#!/usr/bin/env python3
"""Patch v332 -> v333: always scroll to bottom on post open, instantly (no smooth animation)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v332.js'
dst = '_deploy/assets/index-DUcNPOLc-v333.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove !te.current guard + make scroll instant ────────────────────────
# Old: only scrolls when te.current (scrollToComments nav state), smooth window scroll
# New: always scroll to bottom when comments load, instant
OLD_SCROLL = (
    'if(!te.current||A.current||u.length===0)return;'
    'A.current=!0;let e=D.current;'
    'e&&(e.scrollTop=e.scrollHeight),'
    'setTimeout(()=>window.scrollTo({top:document.body.scrollHeight,behavior:`smooth`}),50)'
)
NEW_SCROLL = (
    'if(A.current||u.length===0)return;'
    'A.current=!0;let e=D.current;'
    'if(e){e.scrollTop=e.scrollHeight;}'
    'window.scrollTo({top:document.body.scrollHeight})'
)
if OLD_SCROLL in content:
    content = content.replace(OLD_SCROLL, NEW_SCROLL, 1)
    print('OK: always scroll to bottom instantly on load')
else:
    errors.append('FAIL: scroll useEffect not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
