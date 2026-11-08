#!/usr/bin/env python3
"""Patch v293 -> v294: fix Flock/Activity board missing user posts.
The fetch used created_at ordering with limit=2000; if bots flood recent posts
user posts fall outside that window. Fix: use sort=activity (last_activity DESC)
so posts with recent engagement float to top, and raise limit to 5000 (worker max)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v293.js'
dst = '_deploy/assets/index-DUcNPOLc-v294.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_FETCH = '`${R}/get-posts?limit=2000`'
NEW_FETCH = '`${R}/get-posts?limit=5000&sort=activity`'

if OLD_FETCH in content:
    content = content.replace(OLD_FETCH, NEW_FETCH, 1)
    print('OK: activity board fetch raised to limit=5000 with sort=activity')
else:
    errors.append('FAIL: activity board fetch URL not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
