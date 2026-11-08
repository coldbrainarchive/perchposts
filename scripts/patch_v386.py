#!/usr/bin/env python3
"""Patch v385 -> v386:
- Restore 🔍 to search bar (was accidentally replaced with 🪹)
- Set 🪹 on the post-not-found page (currently still showing 🔍)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v385.js'
dst = '_deploy/assets/index-DUcNPOLc-v386.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restore magnifying glass to search bar ──────────────────────────────────
OLD_SEARCH = 'className:`search-icon`,children:`\U0001fab9`'
NEW_SEARCH = 'className:`search-icon`,children:`\U0001f50d`'
if OLD_SEARCH in content:
    content = content.replace(OLD_SEARCH, NEW_SEARCH, 1)
    print('OK: search bar icon restored to 🔍')
else:
    errors.append('FAIL: search bar icon not found')

# ── 2. Set empty nest on post-not-found page ───────────────────────────────────
OLD_404 = 'children:`Post not found`}),(0,L.jsx)(`div`,{style:{fontSize:13},children:`This post may have been deleted'
# Find the emoji just before this
idx = content.find(OLD_404)
if idx != -1:
    # Find the emoji in the 150 chars before
    before = content[max(0,idx-150):idx]
    if '\U0001f50d' in before:
        start = content.rfind('\U0001f50d', 0, idx)
        content = content[:start] + '\U0001fab9' + content[start+len('\U0001f50d'):]
        print('OK: post-not-found icon set to 🪹')
    else:
        errors.append('FAIL: post-not-found 🔍 not found before heading')
else:
    errors.append('FAIL: post-not-found heading not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
