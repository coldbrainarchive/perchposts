#!/usr/bin/env python3
"""Patch v556 -> v557: Add autocomplete/autocorrect off to search input to stop iOS keyboard suggestions."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v556.js'
dst = '_deploy/assets/index-DUcNPOLc-v557.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('onFocus:()=>a(!0),onKeyDown:e=>{e.key===`Escape`&&(a(!1),s(null)),'
       'e.key===`Backspace`&&!e.target.value&&(q2?ae():m?re():p?ne():f?te():d&&A())},'
       'placeholder:M?`Add keywords to filter…`:`Search or filter by board, region, country…`})')
NEW = ('onFocus:()=>a(!0),onKeyDown:e=>{e.key===`Escape`&&(a(!1),s(null)),'
       'e.key===`Backspace`&&!e.target.value&&(q2?ae():m?re():p?ne():f?te():d&&A())},'
       'placeholder:M?`Add keywords to filter…`:`Search or filter by board, region, country…`,'
       'autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1})')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: autocomplete/autocorrect off added to search input')
else:
    errors.append('FAIL: search input props not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
