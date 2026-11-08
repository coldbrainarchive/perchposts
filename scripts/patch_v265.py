#!/usr/bin/env python3
"""Patch v264 -> v265: fix extra } in DM map closing sequence."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v264.js'
dst = '_deploy/assets/index-DUcNPOLc-v265.js'

content = open(src, encoding='utf-8').read()
errors = []

# Same double-}} issue as before
OLD = '_setDmPickerId(null);}})]})]})]}},_mi);'
NEW = '_setDmPickerId(null);}})]})]})]}`,_mi);'

# Use a cleaner find
cnt = content.count(OLD)
print(f'Found: {cnt}')

if cnt == 1:
    content = content.replace(OLD, '_setDmPickerId(null);}})]})]})]}` + `,_mi);', 1)
else:
    # Try simpler pattern
    OLD2 = ']})]}},_mi);'
    cnt2 = content.count(OLD2)
    print(f'Alt found: {cnt2}')
    if cnt2 == 1:
        content = content.replace(OLD2, ']})]}` + `,_mi);', 1)
    else:
        errors.append('FAIL: target not found')

# Actually just use direct replacement
content2 = open(src, encoding='utf-8').read()
# Find the exact sequence and fix
target = ']})]}},_mi);'
if target in content2:
    content2 = content2.replace(target, ']})]}' + ',_mi);', 1)
    print('OK via content2')
    content = content2

if errors:
    for e in errors: print(e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
