#!/usr/bin/env python3
"""Patch v194 -> v195: hide search bar on post pages."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v194.js'
dst = '_deploy/assets/index-DUcNPOLc-v195.js'

content = open(src, encoding='utf-8').read()
errors = []

# Lr is the search component. $e() = useLocation.
# Add a location check at the top so it returns null on /post/ routes.
OLD = 'function Lr(){let[e,t]=kn(),'
NEW = 'function Lr(){let _loc=$e();if(_loc.pathname.startsWith(`/post/`))return null;let[e,t]=kn(),'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: search bar hidden on post pages')
else:
    errors.append('FAIL: Lr function start not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
