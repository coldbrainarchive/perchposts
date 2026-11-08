#!/usr/bin/env python3
"""Patch v294 -> v295: permanent activity board fix — use server-side activity filter.
Activity board now uses ?activity=1&sort=activity so the worker returns exactly the
right posts (user posts + bot posts with comments) with no client-imposed limit.
Other TagR fetches (board/region/country/user) raised from limit=500 to limit=10000
since the server already filters those by SQL."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v294.js'
dst = '_deploy/assets/index-DUcNPOLc-v295.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Activity board fetch: use server-side activity filter ──────────────────
OLD_TAGR = (
    'u===`activity`?`${R}/get-posts?limit=5000&sort=activity`:`${R}/get-posts?limit=500`'
)
NEW_TAGR = (
    'u===`activity`?`${R}/get-posts?activity=1&sort=activity`:`${R}/get-posts?limit=10000`'
)
if OLD_TAGR in content:
    content = content.replace(OLD_TAGR, NEW_TAGR, 1)
    print('OK: activity board uses server-side filter; other fetches raised to limit=10000')
else:
    errors.append('FAIL: TagR fetch URL not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
