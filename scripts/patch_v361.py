#!/usr/bin/env python3
"""Patch v360 -> v361: move Huddles board to second position in nr array (after Flock)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v360.js'
dst = '_deploy/assets/index-DUcNPOLc-v361.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '{name:`Flock`,slug:`activity`,icon:`\U0001fab6`,virtual:!0},'
    '{name:`General`,slug:`general`,icon:`\U0001f4f0`},'
    '{name:`Sports`,slug:`sports`,icon:`\U0001f3c8`},'
    '{name:`Science`,slug:`science-nature`,icon:`\U0001f52c`},'
    '{name:`Random`,slug:`random`,icon:`\U0001f3b2`},'
    '{name:`Announcements`,slug:`announcements`,icon:`\U0001f4e2`},'
    '{name:`Huddles`,slug:`feedback`,icon:`\U0001f465`}'
)
NEW = (
    '{name:`Flock`,slug:`activity`,icon:`\U0001fab6`,virtual:!0},'
    '{name:`Huddles`,slug:`feedback`,icon:`\U0001f465`},'
    '{name:`General`,slug:`general`,icon:`\U0001f4f0`},'
    '{name:`Sports`,slug:`sports`,icon:`\U0001f3c8`},'
    '{name:`Science`,slug:`science-nature`,icon:`\U0001f52c`},'
    '{name:`Random`,slug:`random`,icon:`\U0001f3b2`},'
    '{name:`Announcements`,slug:`announcements`,icon:`\U0001f4e2`}'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Huddles moved to second position after Flock')
else:
    errors.append('FAIL: boards array not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
