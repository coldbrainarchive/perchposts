#!/usr/bin/env python3
"""Patch v118 -> v119: always run check-jailed on new post page.

The Ur component's useEffect was returning early for logged-in users
(if(e){...return}) so the check-jailed fetch never ran. Caged registered
users would never see the cage notice or have the board locked to The Cage.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v118.js'
dst = '_deploy/assets/index-DUcNPOLc-v119.js'

content = open(src, encoding='utf-8').read()
errors = []

# Remove the early return so check-jailed runs for all users
OLD = 'if(e){n&&f(n);return}let t=Gn();'
NEW = 'if(e&&n)f(n);let t=Gn();'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: removed early return — check-jailed now runs for all users')
else:
    errors.append('FAIL: early return pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
