#!/usr/bin/env python3
"""Patch v117 -> v118: rename Cage board to The Cage throughout the frontend."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v117.js'
dst = '_deploy/assets/index-DUcNPOLc-v118.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Board definition name
OLD_DEF = '{name:`Cage`,slug:`cage`,icon:`\U0001fab9`}'
NEW_DEF = '{name:`The Cage`,slug:`cage`,icon:`\U0001fab9`}'
if OLD_DEF in content:
    content = content.replace(OLD_DEF, NEW_DEF, 1)
    print('OK: board definition renamed to The Cage')
else:
    errors.append('FAIL: board definition not found')

# 2. Main feed & search & trending exclusion filters (all occurrences)
old_excl = 't!==`Cage`&&t!==`Jail`'
new_excl = 't!==`The Cage`&&t!==`Jail`'
count = content.count(old_excl)
if count > 0:
    content = content.replace(old_excl, new_excl)
    print(f'OK: updated {count} feed exclusion filter(s)')
else:
    errors.append('FAIL: feed exclusion filter not found')

old_excl2 = 't2!==`Cage`&&t2!==`Jail`'
new_excl2 = 't2!==`The Cage`&&t2!==`Jail`'
count2 = content.count(old_excl2)
if count2 > 0:
    content = content.replace(old_excl2, new_excl2)
    print(f'OK: updated {count2} t2 exclusion filter(s)')

# 3. Comment handler cage check
OLD_CMT = 'cr(c)!==`Cage`'
NEW_CMT = 'cr(c)!==`The Cage`'
if OLD_CMT in content:
    content = content.replace(OLD_CMT, NEW_CMT, 1)
    print('OK: comment cage check updated')
else:
    errors.append('FAIL: comment cage check not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
