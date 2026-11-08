#!/usr/bin/env python3
"""Patch v170 -> v171: mod uses custom bird emoji; add FLOCK badge in mod panel."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v170.js'
dst = '_deploy/assets/index-DUcNPOLc-v171.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove hardcoded 🐦 for mods — let them fall through to custom bird ────
# Admin keeps 🐧 (special), mods now get their username-based custom bird
OLD_MOD_EMOJI = 'if(e.is_admin)return`\U0001f427`;if(e.is_mod)return`\U0001f426`;'
NEW_MOD_EMOJI = 'if(e.is_admin)return`\U0001f427`;'

if OLD_MOD_EMOJI in content:
    content = content.replace(OLD_MOD_EMOJI, NEW_MOD_EMOJI, 1)
    print('OK: mod now uses custom bird emoji')
else:
    errors.append('FAIL: mod emoji line not found')

# ── 2. Add FLOCK badge for regular members in mod panel member list ────────────
# Currently: after CAGED badge there's nothing for regular users.
# Add a muted FLOCK badge when user is neither mod, admin, banned, nor caged.
OLD_CAGED_BADGE = (
    'c&&!s&&(0,L.jsx)(`span`,{style:{fontSize:10,fontWeight:700,'
    'color:`#fbbf24`,background:`rgba(251,191,36,0.12)`,padding:`1px 6px`,'
    'borderRadius:999},children:`CAGED`})'
)
NEW_CAGED_BADGE = (
    'c&&!s&&(0,L.jsx)(`span`,{style:{fontSize:10,fontWeight:700,'
    'color:`#fbbf24`,background:`rgba(251,191,36,0.12)`,padding:`1px 6px`,'
    'borderRadius:999},children:`CAGED`}),'
    '!f&&!s&&!c&&(0,L.jsx)(`span`,{style:{fontSize:10,fontWeight:700,'
    'color:`#64748b`,background:`rgba(100,116,139,0.12)`,padding:`1px 6px`,'
    'borderRadius:999},children:`FLOCK`})'
)

if OLD_CAGED_BADGE in content:
    content = content.replace(OLD_CAGED_BADGE, NEW_CAGED_BADGE, 1)
    print('OK: FLOCK badge added for regular members in mod panel')
else:
    errors.append('FAIL: CAGED badge not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
