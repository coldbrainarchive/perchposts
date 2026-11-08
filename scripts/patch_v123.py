#!/usr/bin/env python3
"""Patch v122 -> v123: update cage message text."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v122.js'
dst = '_deploy/assets/index-DUcNPOLc-v123.js'

content = open(src, encoding='utf-8').read()
errors = []

# Unicode curly apostrophe ’ in "You're"
OLD_MSG = "You’re Caged! You can only post and comment in \U0001fab9 The Cage"
NEW_MSG = 'You’re Caged! You can only post and comment in “The Cage”'

count = content.count(OLD_MSG)
if count:
    content = content.replace(OLD_MSG, NEW_MSG)
    print(f'OK: updated {count} cage message(s)')
else:
    errors.append(f'FAIL: not found (sample: {repr(OLD_MSG[:30])})')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
