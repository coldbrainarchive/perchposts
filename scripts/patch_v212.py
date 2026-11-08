#!/usr/bin/env python3
"""Patch v211 -> v212: Sports → yellow, Science → green."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v211.js'
dst = '_deploy/assets/index-DUcNPOLc-v212.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'sports:`#4ade80`,"science-nature":`#818cf8`'
NEW = 'sports:`#facc15`,"science-nature":`#4ade80`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Sports → yellow, Science → green')
else:
    errors.append('FAIL: colour map not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
