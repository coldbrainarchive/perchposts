#!/usr/bin/env python3
"""Patch v429 -> v430:
Xn: make `o` (admin flag for white background) also check i.hat (Jn result),
so _adminUsers-detected admins get white background even when is_admin is false.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v429.js'
dst = '_deploy/assets/index-DUcNPOLc-v430.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'let i=Jn(e),a=e?.browser_id&&String(e.browser_id).startsWith(`bot-`),o=!a&&e?.is_admin===!0,s=!a&&!o&&e?.is_mod===!0'
NEW = 'let i=Jn(e),a=e?.browser_id&&String(e.browser_id).startsWith(`bot-`),o=!a&&(e?.is_admin===!0||!!(i&&i.hat)),s=!a&&!o&&e?.is_mod===!0'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Xn o uses i.hat so _adminUsers drives white background too')
else:
    errors.append('FAIL: Xn o= line not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
