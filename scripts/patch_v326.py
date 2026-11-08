#!/usr/bin/env python3
"""Patch v325 -> v326: fix emoji keyboard not opening.
iOS requires focus() to be called synchronously in the click handler.
setTimeout breaks this. Remove it — the input is already in the DOM (no display:none)
so synchronous focus() works fine and opens the native emoji keyboard."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v325.js'
dst = '_deploy/assets/index-DUcNPOLc-v326.js'

content = open(src, encoding='utf-8').read()
errors = []

# Revert setTimeout back to synchronous focus
OLD_D = 'function D(){y(!1),x(!0),setTimeout(()=>{S.current&&(S.current.value=``,S.current.focus())},20)}'
NEW_D = 'function D(){y(!1),x(!0),S.current&&(S.current.value=``,S.current.focus())}'
if OLD_D in content:
    content = content.replace(OLD_D, NEW_D, 1)
    print('OK: focus() made synchronous again (iOS keyboard requirement)')
else:
    errors.append('FAIL: D() with setTimeout not found')

# Also remove pointer-events:none so touch also works as fallback
OLD_CSS = '        pointer-events: none;\n        border: none;\n'
NEW_CSS = '        border: none;\n'
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: pointer-events:none removed from emoji input')
else:
    errors.append('FAIL: pointer-events CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
