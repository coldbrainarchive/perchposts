#!/usr/bin/env python3
"""Patch v226 -> v227: Flock sorts by created_at DESC so all posts appear in chronological order."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v226.js'
dst = '_deploy/assets/index-DUcNPOLc-v227.js'

content = open(src, encoding='utf-8').read()
errors = []

# Change Flock server fetch from sort=activity to no sort (default created_at DESC)
OLD = '`${R}/get-posts?limit=2000&sort=activity`'
NEW = '`${R}/get-posts?limit=2000`'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Flock fetches by created_at DESC')
else:
    errors.append('FAIL: Flock fetch URL not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
