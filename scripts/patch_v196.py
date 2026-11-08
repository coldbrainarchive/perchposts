#!/usr/bin/env python3
"""Patch v195 -> v196: add top padding to post page matching the section gap."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v195.js'
dst = '_deploy/assets/index-DUcNPOLc-v196.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '.home-shell {\n'
    '        display: block;\n'
    '        width: min(1280px, 100%);\n'
    '        margin: 0 auto;\n'
    '        padding: 0 20px 32px;\n'
    '        box-sizing: border-box;\n'
    '      }'
)
NEW = (
    '.home-shell {\n'
    '        display: block;\n'
    '        width: min(1280px, 100%);\n'
    '        margin: 0 auto;\n'
    '        padding: 18px 20px 32px;\n'
    '        box-sizing: border-box;\n'
    '      }'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: top padding added to home-shell')
else:
    errors.append('FAIL: .home-shell CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
