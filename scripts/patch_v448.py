#!/usr/bin/env python3
"""Patch v447 -> v448:
Main search input: add autoComplete/autoCorrect/autoCapitalize/spellCheck off
to prevent iOS Safari text processing from fighting React's controlled value
and jumping the cursor when the results dropdown renders.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v447.js'
dst = '_deploy/assets/index-DUcNPOLc-v448.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'ref:c,className:`search-input`,value:n,onChange:e=>{r(e.target.value),s(null)},onFocus:()=>a(!0),'
NEW = 'ref:c,className:`search-input`,value:n,autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,onChange:e=>{r(e.target.value),s(null)},onFocus:()=>a(!0),'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: search input autocomplete/correct/capitalize disabled')
else:
    errors.append('FAIL: main search input not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
