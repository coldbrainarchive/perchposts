#!/usr/bin/env python3
"""Patch v238 -> v239: fix missing closing paren after null children."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v238.js'
dst = '_deploy/assets/index-DUcNPOLc-v239.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'children:null},(()=>'
NEW  = 'children:null}),(()=>'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: closing paren added')
else:
    errors.append('FAIL: target string not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
