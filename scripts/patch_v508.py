#!/usr/bin/env python3
"""Patch v507 -> v508: Make comment header bar match user pill dimensions."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v507.js'
dst = '_deploy/assets/index-DUcNPOLc-v508.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. CSS: reduce padding and gap to match pill ─────────────────────────────
OLD_CSS = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 3px 10px;\n      }'
NEW_CSS = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 4px;\n        padding: 2px 8px;\n      }'
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: chat-msg-meta padding/gap reduced')
else:
    errors.append('FAIL: chat-msg-meta CSS not found')

# ── 2. JSX: shrink bird from 17px/_bsz+2 to 16px/_bsz (matches pill) ────────
OLD_BIRD = 'position:`relative`,display:`inline-flex`,alignItems:`center`,justifyContent:`center`,fontSize:_bsz+2,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`'
NEW_BIRD = 'position:`relative`,display:`inline-flex`,alignItems:`center`,justifyContent:`center`,fontSize:_bsz,lineHeight:1,flexShrink:0,width:`16px`,height:`16px`'
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: bird shrunk to 16px to match pill')
else:
    errors.append('FAIL: bird style in chat-msg-meta not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
