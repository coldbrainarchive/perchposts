#!/usr/bin/env python3
"""Patch v218 -> v219: close search dropdown immediately on board select; continent stays open."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v218.js'
dst = '_deploy/assets/index-DUcNPOLc-v219.js'

content = open(src, encoding='utf-8').read()
errors = []

# ee = board select. Currently keeps dropdown open (calls c.current?.focus()).
# Close it instead: a(!1) closes dropdown, s(null) clears continent drill-down.
OLD = 'function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),r(``),s(null),c.current?.focus()}'
NEW = 'function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),r(``),s(null),a(!1)}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: board select closes dropdown')
else:
    errors.append('FAIL: ee function not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
