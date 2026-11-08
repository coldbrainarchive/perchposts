#!/usr/bin/env python3
"""Patch v277 -> v278: remove SRLoading bar (causes weird visual bar), remove
admin/mod role badges from user search results."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v277.js'
dst = '_deploy/assets/index-DUcNPOLc-v278.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove SRLoading "Searching…" bar from home-feed ──────────────────────
OLD_LOADING = (
    'm&&SRLoading&&(0,L.jsx)(`div`,{style:{padding:`32px 20px`,textAlign:`center`,color:`#64748b`,fontSize:13},children:`Searching…`}),'
)
if OLD_LOADING in content:
    content = content.replace(OLD_LOADING, '', 1)
    print('OK: SRLoading bar removed')
else:
    errors.append('FAIL: SRLoading bar not found')

# ── 2. Remove admin badge from user result items ──────────────────────────────
OLD_ADMIN_BADGE = (
    '_ur.role===`admin`&&(0,L.jsx)(`span`,{style:{fontSize:10,background:`#fff`,color:`#000`,borderRadius:4,padding:`1px 5px`,fontWeight:700},children:`admin`}),'
)
if OLD_ADMIN_BADGE in content:
    content = content.replace(OLD_ADMIN_BADGE, '', 1)
    print('OK: admin badge removed from user results')
else:
    errors.append('FAIL: admin badge not found')

# ── 3. Remove mod badge from user result items ────────────────────────────────
OLD_MOD_BADGE = (
    '_ur.role===`mod`&&(0,L.jsx)(`span`,{style:{fontSize:10,background:`#c084fc`,color:`#14081d`,borderRadius:4,padding:`1px 5px`,fontWeight:700},children:`mod`})'
)
if OLD_MOD_BADGE in content:
    content = content.replace(OLD_MOD_BADGE, '', 1)
    print('OK: mod badge removed from user results')
else:
    errors.append('FAIL: mod badge not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
