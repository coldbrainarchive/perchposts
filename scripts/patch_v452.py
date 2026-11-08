#!/usr/bin/env python3
"""Patch v451 -> v452:
- Remove type="search" (causes visual cursor glitch on iOS, native clear button conflicts)
- Fix ie() clear button to also clear the uncontrolled input DOM value via ref
- Keep autoComplete="search" to suppress AutoFill Contact
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v451.js'
dst = '_deploy/assets/index-DUcNPOLc-v452.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove type="search" from input ───────────────────────────────────────
OLD_TYPE = ('key:`si`,ref:c,type:`search`,className:`search-input`,defaultValue:n,'
            'autoComplete:`search`')
NEW_TYPE = ('key:`si`,ref:c,className:`search-input`,defaultValue:n,'
            'autoComplete:`search`')
if OLD_TYPE in content:
    content = content.replace(OLD_TYPE, NEW_TYPE, 1)
    print('OK: type="search" removed')
else:
    errors.append('FAIL: type=search input not found')

# ── 2. Fix ie() to also clear the uncontrolled DOM input value ────────────────
OLD_IE = 'function ie(){r(``);let n=new URLSearchParams(e);n.delete(`q`),t(n,{replace:!0})}'
NEW_IE = 'function ie(){r(``);if(c.current)c.current.value=``;let n=new URLSearchParams(e);n.delete(`q`),t(n,{replace:!0})}'
if OLD_IE in content:
    content = content.replace(OLD_IE, NEW_IE, 1)
    print('OK: ie() clears DOM input value via ref')
else:
    errors.append('FAIL: ie() not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
