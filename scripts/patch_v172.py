#!/usr/bin/env python3
"""Patch v171 -> v172: show rank/stats for admin; admin uses custom bird in pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v171.js'
dst = '_deploy/assets/index-DUcNPOLc-v172.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove hardcoded 🐧 for admin — fall through to custom bird ─────────────
OLD_ADMIN = 'if(e.is_admin)return`\U0001f427`;var _s'
NEW_ADMIN = 'var _s'
if OLD_ADMIN in content:
    content = content.replace(OLD_ADMIN, NEW_ADMIN, 1)
    print('OK: admin now uses custom bird emoji')
else:
    errors.append('FAIL: admin emoji return not found')

# ── 2. Show rank/stats card for all logged-in users, not just regular flock ────
OLD_GATE = '(e&&!D)?(0,L.jsxs)(`div`,{className:`content-card`'
NEW_GATE = 'e?(0,L.jsxs)(`div`,{className:`content-card`'
if OLD_GATE in content:
    content = content.replace(OLD_GATE, NEW_GATE, 1)
    print('OK: rank/stats card shown for all logged-in users')
else:
    errors.append('FAIL: rank card gate not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
