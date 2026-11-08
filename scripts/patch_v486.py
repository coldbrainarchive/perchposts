#!/usr/bin/env python3
"""Patch v474 -> v486:
- Both slide-up panels (notifications + sign-in): background #1a1d27 → #0b0f12
- User info card: remove border/radius so it blends flush into the black top
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v486.js'

content = open(src, encoding='utf-8').read()
errors = []

# Both panel backgrounds → #0b0f12
OLD_PANEL = 'position:`relative`,background:`#1a1d27`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`'
NEW_PANEL = 'position:`relative`,background:`#0b0f12`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`'
n = content.count(OLD_PANEL)
if n > 0:
    content = content.replace(OLD_PANEL, NEW_PANEL)
    print(f'OK: {n} panel(s) → #0b0f12')
else:
    errors.append('FAIL: panel background')

# User info card: flush black, no border/radius
OLD_CARD = 'background:`#161920`,borderRadius:14,border:`1px solid #2e303a`'
NEW_CARD = 'background:`#0b0f12`,borderRadius:0,border:`none`'
if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD, 1)
    print('OK: user info card → flush black')
else:
    errors.append('FAIL: user info card')

if errors:
    print('\nERRORS:'); [print(' ',e) for e in errors]; sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
