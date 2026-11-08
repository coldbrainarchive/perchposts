#!/usr/bin/env python3
"""Patch v213 -> v214: new colours for Random (violet), Announcements (pink), Feedback (orange)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v213.js'
dst = '_deploy/assets/index-DUcNPOLc-v214.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'random:`#f87171`,announcements:`#facc15`,feedback:`#2dd4bf`'
NEW = 'random:`#a78bfa`,announcements:`#f472b6`,feedback:`#fb923c`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Random → violet, Announcements → pink, Feedback → orange')
else:
    errors.append('FAIL: colour map not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
