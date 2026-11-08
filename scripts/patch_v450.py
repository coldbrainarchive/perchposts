#!/usr/bin/env python3
"""Patch v449 -> v450:
Convert main search input from controlled (value=n) to uncontrolled (defaultValue=n).
React won't touch the DOM value during re-renders, eliminating cursor jumps entirely.
onChange still updates n state for clear-button/placeholder logic.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v449.js'
dst = '_deploy/assets/index-DUcNPOLc-v450.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('ref:c,className:`search-input`,value:n,'
       'autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,'
       'onChange:e=>{r(e.target.value),s(null)}')
NEW = ('ref:c,className:`search-input`,defaultValue:n,'
       'autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,'
       'onChange:e=>{r(e.target.value),s(null)}')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: search input is now uncontrolled (defaultValue) — cursor safe')
else:
    errors.append('FAIL: search input not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
