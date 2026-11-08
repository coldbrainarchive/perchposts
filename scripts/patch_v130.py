#!/usr/bin/env python3
"""Patch v129 -> v130: solid colour user pills with black text, site-wide."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v129.js'
dst = '_deploy/assets/index-DUcNPOLc-v130.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Update Xn component: solid bg + black text for regular users
OLD_XN_STYLE = (
    'color:(o||s)?`#0a0a0a`:N?`#ffffff`:c,'
    'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:`${c}18`,'
    'borderColor:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:`${c}55`'
)
NEW_XN_STYLE = (
    'color:N?`#ffffff`:`#0a0a0a`,'
    'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
    'borderColor:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c'
)
if OLD_XN_STYLE in content:
    content = content.replace(OLD_XN_STYLE, NEW_XN_STYLE, 1)
    print('OK: Xn pill — solid colour, black text')
else:
    errors.append('FAIL: Xn style not found')

# 2. Update signup bird pill: solid bg + black text
OLD_SIGNUP_BG = "background:_gu?Hn(null,_gu).replace('hsl(','hsla(').replace(')',', 0.12)'):`transparent`"
NEW_SIGNUP_BG = 'background:_gu?Hn(null,_gu):`transparent`'
if OLD_SIGNUP_BG in content:
    content = content.replace(OLD_SIGNUP_BG, NEW_SIGNUP_BG, 1)
    print('OK: signup pill — solid colour background')
else:
    errors.append('FAIL: signup pill background not found')

OLD_SIGNUP_TEXT = 'color:_gu?Hn(null,_gu):`#64748b`'
NEW_SIGNUP_TEXT = 'color:_gu?`#0a0a0a`:`#64748b`'
if OLD_SIGNUP_TEXT in content:
    content = content.replace(OLD_SIGNUP_TEXT, NEW_SIGNUP_TEXT, 1)
    print('OK: signup pill — black text on solid colour')
else:
    errors.append('FAIL: signup pill text colour not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
