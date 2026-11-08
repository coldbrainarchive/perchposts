#!/usr/bin/env python3
"""Patch v453 -> v454:
Debounce the search state update (r) that drives the user-search dropdown.
The dropdown appearing mid-keystroke causes a layout shift that confuses
Safari's cursor tracking. By delaying r() 250ms, the dropdown only shows
after the user pauses, eliminating the cursor jump/glitch entirely.
s(null) still fires immediately so selected-user state clears without delay.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v453.js'
dst = '_deploy/assets/index-DUcNPOLc-v454.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'onChange:e=>{r(e.target.value),s(null)}'
NEW = 'onChange:e=>{const _sv=e.target.value;s(null);if(c.current){clearTimeout(c.current._dbt);c.current._dbt=setTimeout(()=>r(_sv),250);}else{r(_sv);}}'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: search onChange debounced 250ms')
else:
    errors.append('FAIL: search onChange not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
