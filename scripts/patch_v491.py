#!/usr/bin/env python3
"""Patch v490 -> v491: Make all sign-in/notification panel backgrounds match
the nav bar color #0b0f12 — bottom sheets, desktop sidebar, mobile DM view."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v490.js'
dst = '_deploy/assets/index-DUcNPOLc-v491.js'

content = open(src, encoding='utf-8').read()
errors = []

# Both bottom-sheet panels (#1a1d27 → #0b0f12)
OLD1 = 'background:`#1a1d27`,borderRadius:`20px 20px 0 0`'
NEW1 = 'background:`#0b0f12`,borderRadius:`20px 20px 0 0`'
n = content.count(OLD1)
if n > 0:
    content = content.replace(OLD1, NEW1)
    print(f'OK: {n} bottom-sheet panel(s) → #0b0f12')
else:
    errors.append('FAIL: bottom sheets')

# Desktop sidebar gradient
OLD2 = 'background:`linear-gradient(180deg, #1b1d24 0%, #14161c 100%)`'
NEW2 = 'background:`#0b0f12`'
if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    print('OK: desktop sidebar → #0b0f12')
else:
    errors.append('FAIL: desktop sidebar')

# Mobile DM view
OLD3 = 'background:`#13151c`,zIndex:200'
NEW3 = 'background:`#0b0f12`,zIndex:200'
if OLD3 in content:
    content = content.replace(OLD3, NEW3, 1)
    print('OK: mobile DM panel → #0b0f12')
else:
    errors.append('FAIL: mobile DM')

if errors:
    print('\nERRORS:'); [print(' ',e) for e in errors]; sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
