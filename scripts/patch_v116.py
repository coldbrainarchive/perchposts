#!/usr/bin/env python3
"""Patch v115 -> v116: fix board tag filter incorrectly excluding cage posts."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v115.js'
dst = '_deploy/assets/index-DUcNPOLc-v116.js'

content = open(src, encoding='utf-8').read()
errors = []

# The tag/board filter view was running the same cage-exclusion filter as the
# main feed, meaning Cage board showed nothing even when explicitly selected.
# Fix: remove cage/jail exclusion from the board-specific tag filter.
OLD = 'setTagR(Sr((d2.posts||[]).filter(e2=>{const t2=cr(e2);return t2!==`Cage`&&t2!==`Jail`&&(!e2.pinned||e2.pinned_global)})))'
NEW = 'setTagR(Sr(d2.posts||[]))'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: removed cage/jail exclusion from board tag filter')
else:
    errors.append('FAIL: board tag filter pattern not found')
    idx = content.find('setTagR(Sr(')
    if idx >= 0:
        print(f'  Found setTagR at {idx}: {repr(content[idx:idx+150])}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
