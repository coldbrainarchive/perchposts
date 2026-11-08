#!/usr/bin/env python3
"""Patch v116 -> v117: update cage notice and alert text."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v116.js'
dst = '_deploy/assets/index-DUcNPOLc-v117.js'

content = open(src, encoding='utf-8').read()
errors = []

NEW_MSG = "You’re caged — you can only post and comment in \U0001fab9 The Cage"

# 1. Notice banner on new post page
OLD_BANNER = '\U0001fab9 You’ve been caged — you can only post and comment in the Cage tag.'
NEW_BANNER = NEW_MSG
if OLD_BANNER in content:
    content = content.replace(OLD_BANNER, NEW_BANNER, 1)
    print('OK: cage notice banner updated')
else:
    errors.append('FAIL: cage notice banner not found')

# 2. All three alert() calls
OLD_ALERT = 'alert("You\'re caged — you can only post and comment in the Cage")'
NEW_ALERT = f'alert("{NEW_MSG}")'
count = content.count(OLD_ALERT)
if count > 0:
    content = content.replace(OLD_ALERT, NEW_ALERT)
    print(f'OK: updated {count} cage alert(s)')
else:
    errors.append('FAIL: cage alert not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
