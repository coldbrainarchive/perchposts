#!/usr/bin/env python3
"""Patch v558 -> v559: Board selection closes dropdown — remove focus() call from ee()
so a(!1) actually closes the menu instead of re-opening it via onFocus."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v558.js'
dst = '_deploy/assets/index-DUcNPOLc-v559.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),r(``),s(null),a(!1);'
       'if(c.current){c.current.value=``;c.current.focus();}}')
NEW = ('function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),r(``),s(null),a(!1);'
       'if(c.current){c.current.value=``;c.current.blur();}}')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: board select closes dropdown (blur instead of focus)')
else:
    errors.append('FAIL: ee function not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
