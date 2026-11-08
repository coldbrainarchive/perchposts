#!/usr/bin/env python3
"""Patch v450 -> v451:
- type="search": tells iOS this is a search field, suppresses AutoFill Contact popup
  (the AutoFill bar was stealing focus and resetting the cursor to 0)
- key="si": stable key prevents React from ever unmounting/remounting the input
  even when surrounding filter chips change
- autoComplete="search": reinforces to iOS that this is a search field
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v450.js'
dst = '_deploy/assets/index-DUcNPOLc-v451.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('ref:c,className:`search-input`,defaultValue:n,'
       'autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,')
NEW = ('key:`si`,ref:c,type:`search`,className:`search-input`,defaultValue:n,'
       'autoComplete:`search`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: type=search, key=si, autoComplete=search applied')
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
