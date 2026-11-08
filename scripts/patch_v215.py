#!/usr/bin/env python3
"""Patch v214 -> v215: rename Feedback board to Questions."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v214.js'
dst = '_deploy/assets/index-DUcNPOLc-v215.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '{name:`Feedback`,slug:`feedback`,icon:`💬`}'
NEW = '{name:`Questions`,slug:`feedback`,icon:`💬`}'

if OLD in content:
    content = content.replace(OLD, NEW)
    print('OK: Feedback → Questions')
else:
    errors.append('FAIL: Feedback board not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
