#!/usr/bin/env python3
"""Patch v237 -> v238: fix double-comma syntax error left by Utilities removal."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v237.js'
dst = '_deploy/assets/index-DUcNPOLc-v238.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'gap:16,marginBottom:24},children:null},,(()=>'
NEW = 'gap:16,marginBottom:24},children:null},(()=>'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: double comma fixed')
else:
    errors.append('FAIL: double comma not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
