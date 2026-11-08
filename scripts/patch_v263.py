#!/usr/bin/env python3
"""Patch v262 -> v263: fix extra } in DM message map closing sequence."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v262.js'
dst = '_deploy/assets/index-DUcNPOLc-v263.js'

content = open(src, encoding='utf-8').read()
errors = []

# The chat-msg closing has }}, should be single }
OLD = 'chat-reaction-pill`,children:[_em,` `,_us.length]},_em))})]})]}},_mi);})'
NEW = 'chat-reaction-pill`,children:[_em,` `,_us.length]},_em))})]})]}` + `,_mi);})'

# Need to check exact string
idx = content.find('_us.length]},_em))})]})]}},_mi);})')
print('Found double }}:', idx != -1)
if idx != -1:
    print(repr(content[idx:idx+50]))

OLD = '})]})]}},_mi);}'
NEW = '})]})]}`,_mi);}'

# Use simpler replacement
OLD2 = 'children:[_em,` `,_us.length]},_em))})]})]}},_mi);'
NEW2 = 'children:[_em,` `,_us.length]},_em))})]})]}` + `,_mi);'

# Even simpler - just fix the double brace
OLD3 = ']}},_mi);'
NEW3 = ']},_mi);'

cnt = content.count(OLD3)
print(f'"{OLD3}" count:', cnt)
if cnt == 1:
    content = content.replace(OLD3, NEW3, 1)
    print('OK: double }} fixed to single }')
else:
    errors.append(f'FAIL: found {cnt} occurrences of target')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
