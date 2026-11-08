#!/usr/bin/env python3
"""Patch v417 -> v418:
- OP label: use username comparison when available (not browser_id)
- Right-side bubble: use username to identify own messages across devices
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v417.js'
dst = '_deploy/assets/index-DUcNPOLc-v418.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. OP flag: prefer username over browser_id ───────────────────────────────
OLD_OP = 'let g=e.browser_id===t&&(n?e.username===n:!e.username)'
NEW_OP = 'let g=n?e.username===n:(e.browser_id===t&&!e.username)'
if OLD_OP in content:
    content = content.replace(OLD_OP, NEW_OP, 1)
    print('OK: OP flag uses username-first comparison')
else:
    errors.append('FAIL: OP flag expression not found')

# ── 2. "Is me" flag: prefer username over browser_id ─────────────────────────
OLD_ME = '_isMe=e.browser_id===Gn()&&(_myUn?e.username===_myUn:!e.username)'
NEW_ME = '_isMe=_myUn?e.username===_myUn:(e.browser_id===Gn()&&!e.username)'
if OLD_ME in content:
    content = content.replace(OLD_ME, NEW_ME, 1)
    print('OK: isMe flag uses username-first comparison')
else:
    errors.append('FAIL: isMe flag expression not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
