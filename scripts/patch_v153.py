#!/usr/bin/env python3
"""Patch v152 -> v153: force pill width + centering with !important on mobile."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v152.js'
dst = '_deploy/assets/index-DUcNPOLc-v153.js'

content = open(src, encoding='utf-8').read()
errors = []

# width:max-content is ignored because the span gets blockified as a flex item
# and fills its container. !important overrides both the blockification AND any
# inline styles, so this is the only reliable way to pin the pill's width.
OLD_MQ = (
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
NEW_MQ = (
    '@media (max-width: 900px) {\n'
    '        .nav-user-pill .user-pill-name {\n'
    '          display: none;\n'
    '        }\n'
    '        .nav-user-pill .user-pill {\n'
    '          width: 30px !important;\n'
    '          padding: 0 !important;\n'
    '          justify-content: center !important;\n'
    '          gap: 0 !important;\n'
    '        }\n'
    '      }'
)

if OLD_MQ in content:
    content = content.replace(OLD_MQ, NEW_MQ, 1)
    print('OK: nav pill forced to 30px centred with !important')
else:
    errors.append('FAIL: media query not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
