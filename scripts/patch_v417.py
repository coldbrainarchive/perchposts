#!/usr/bin/env python3
"""Patch v416 -> v417:
- Rename "Chats" -> "Chirps" in post page comment count header
- Centre "No chirps yet" placeholder vertically and horizontally
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v416.js'
dst = '_deploy/assets/index-DUcNPOLc-v417.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Rename "Chats" → "Chirps" ──────────────────────────────────────────────
OLD_CHATS = '` Chats`'
NEW_CHATS = '` Chirps`'
if OLD_CHATS in content:
    content = content.replace(OLD_CHATS, NEW_CHATS, 1)
    print('OK: renamed Chats -> Chirps')
else:
    errors.append('FAIL: " Chats" string not found')

# ── 2. Centre "No chirps yet" placeholder both axes ───────────────────────────
OLD_PH = '(0,L.jsx)(`p`,{style:{textAlign:`center`,color:`rgba(148,163,184,0.3)`,fontSize:13,padding:`16px 0`,margin:0},children:`No chirps yet`})'
NEW_PH = '(0,L.jsx)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`center`,flex:1,minHeight:120},children:(0,L.jsx)(`p`,{style:{color:`rgba(148,163,184,0.3)`,fontSize:13,margin:0},children:`No chirps yet`})})'
if OLD_PH in content:
    content = content.replace(OLD_PH, NEW_PH, 1)
    print('OK: "No chirps yet" centred both axes')
else:
    errors.append('FAIL: "No chirps yet" placeholder not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
