#!/usr/bin/env python3
"""Patch v243 -> v244: add missing ) closing the restored notifications useEffect."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v243.js'
dst = '_deploy/assets/index-DUcNPOLc-v244.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'v(!1)})())},[c,e,r];(0,_.useEffect)'
NEW  = 'v(!1)})())},[c,e,r]);(0,_.useEffect)'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: ) added to close notifications useEffect')
else:
    errors.append('FAIL: notifications effect end not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

opens_p = content.count('(')
closes_p = content.count(')')
print(f'Parens: {opens_p-closes_p}, Braces: {content.count("{")-content.count("}")}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
