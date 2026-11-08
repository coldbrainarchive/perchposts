#!/usr/bin/env python3
"""Patch v135 -> v136: fix invalid \` escape — use single-quoted emoji in array."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v135.js'
dst = '_deploy/assets/index-DUcNPOLc-v136.js'

content = open(src, encoding='utf-8').read()
errors = []

# Fix the broken backtick-escaped array in Jn
# The bug: [\`🐤\`,\`🐦\`,\`🐧\`] — \` is invalid outside a template literal
OLD_BIRDS = "[\`\U0001f424\`,\`\U0001f426\`,\`\U0001f427\`]"
NEW_BIRDS = "['🐤','🐦','🐧']"

count = content.count(OLD_BIRDS)
if count > 0:
    content = content.replace(OLD_BIRDS, NEW_BIRDS)
    print(f'OK: fixed {count} broken emoji array(s)')
else:
    # Try alternate form that Python might have produced
    OLD_BIRDS2 = '[`🐤`,`🐦`,`🐧`]'
    if OLD_BIRDS2 in content:
        content = content.replace(OLD_BIRDS2, NEW_BIRDS)
        print('OK: fixed emoji array (alt form)')
    else:
        errors.append('FAIL: broken birds array not found')
        # Show what we have
        idx = content.find('_e=')
        if idx >= 0:
            print(f'  Found _e= at {idx}: {repr(content[idx:idx+50])}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
