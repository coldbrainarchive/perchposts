#!/usr/bin/env python3
"""Patch v164 -> v165: fix missing } in header center column close sequence."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v164.js'
dst = '_deploy/assets/index-DUcNPOLc-v165.js'

content = open(src, encoding='utf-8').read()
errors = []

# The center column jsxs div was closed with ]})] (missing }) instead of ]})]})
OLD = '`Change password`})]})]):null,'
NEW = '`Change password`})]})]}):null,'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: fixed missing } in center column close')
else:
    errors.append('FAIL: broken close sequence not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
