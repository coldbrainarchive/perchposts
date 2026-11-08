#!/usr/bin/env python3
"""Patch v146 -> v147: centre bird badge in collapsed nav pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v146.js'
dst = '_deploy/assets/index-DUcNPOLc-v147.js'

content = open(src, encoding='utf-8').read()
errors = []

# When the username is hidden the pill still has asymmetric padding (0 9px 0 6px)
# and a gap, so the badge drifts left. Fix: in the same media query, override
# the nav pill to justify-content:center and use equal padding.
OLD_MQ = (
    '@media (max-width: 900px) {\n'
    '        .nav-user-pill .user-pill-name {\n'
    '          display: none;\n'
    '        }\n'
    '      }'
)
NEW_MQ = (
    '@media (max-width: 900px) {\n'
    '        .nav-user-pill .user-pill-name {\n'
    '          display: none;\n'
    '        }\n'
    '        .nav-user-pill .user-pill {\n'
    '          justify-content: center;\n'
    '          padding: 0 7px;\n'
    '          gap: 0;\n'
    '        }\n'
    '      }'
)

if OLD_MQ in content:
    content = content.replace(OLD_MQ, NEW_MQ, 1)
    print('OK: collapsed nav pill centred')
else:
    errors.append('FAIL: mobile media query not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
