#!/usr/bin/env python3
"""Patch v112 -> v113: remove debug logs."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v112.js'
dst = '_deploy/assets/index-DUcNPOLc-v113.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD1 = 'console.log("[CAGE]",{p,h,board:(sr(h)||nr[0]).name,ls:localStorage.getItem("_caged")});'
if OLD1 in content:
    content = content.replace(OLD1, '', 1)
    print('OK: removed [CAGE] debug log')
else:
    errors.append('FAIL: [CAGE] debug log not found')

OLD2 = 'console.log("[POST-ERR]",g);'
if OLD2 in content:
    content = content.replace(OLD2, '', 1)
    print('OK: removed [POST-ERR] debug log')
else:
    errors.append('FAIL: [POST-ERR] debug log not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
