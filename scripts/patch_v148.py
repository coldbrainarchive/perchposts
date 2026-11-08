#!/usr/bin/env python3
"""Patch v147 -> v148: centre collapsed nav pill at the button level."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v147.js'
dst = '_deploy/assets/index-DUcNPOLc-v148.js'

content = open(src, encoding='utf-8').read()
errors = []

# The outer nav-user-pill button is display:flex without justify-content,
# so the inner pill sits at flex-start.  Fix: centre at the button level and
# revert the bad inner-pill override (justify-content on inline-flex caused
# the badge to shift further left, not right).
OLD_MQ = (
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
NEW_MQ = (
    '@media (max-width: 900px) {\n'
    '        .nav-user-pill .user-pill-name {\n'
    '          display: none;\n'
    '        }\n'
    '        .nav-user-pill {\n'
    '          justify-content: center;\n'
    '          align-items: center;\n'
    '        }\n'
    '        .nav-user-pill .user-pill {\n'
    '          padding: 0 8px;\n'
    '        }\n'
    '      }'
)

if OLD_MQ in content:
    content = content.replace(OLD_MQ, NEW_MQ, 1)
    print('OK: nav-user-pill centred at button level')
else:
    errors.append('FAIL: media query not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
