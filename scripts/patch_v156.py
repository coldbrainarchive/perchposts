#!/usr/bin/env python3
"""Patch v155 -> v156: remove width:fit-content (broke Chrome), fix padding inline."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v155.js'
dst = '_deploy/assets/index-DUcNPOLc-v156.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Remove width:fit-content from pill inline style (computed differently per
#    browser — Chrome made the pill tiny). Keep justifyContent:center and add
#    equal padding inline so badge is centred unconditionally.
OLD_PILL_INLINE = (
    'cursor:r?`pointer`:`default`,'
    'justifyContent:`center`,width:`fit-content`}'
)
NEW_PILL_INLINE = (
    'cursor:r?`pointer`:`default`,'
    'justifyContent:`center`,padding:`0 8px`}'
)
if OLD_PILL_INLINE in content:
    content = content.replace(OLD_PILL_INLINE, NEW_PILL_INLINE, 1)
    print('OK: replaced fit-content with padding:0 8px in pill inline style')
else:
    errors.append('FAIL: pill inline style not found')

# 2. Remove width:max-content from base .user-pill CSS (added in v151, unneeded
#    and conflicts with the inline padding approach).
OLD_PILL_CSS = (
    'display: inline-flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        height: 22px;\n'
    '        width: max-content;\n'
    '        padding: 0 8px;\n'
)
NEW_PILL_CSS = (
    'display: inline-flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        height: 22px;\n'
    '        padding: 0 9px 0 6px;\n'
)
if OLD_PILL_CSS in content:
    content = content.replace(OLD_PILL_CSS, NEW_PILL_CSS, 1)
    print('OK: base .user-pill CSS restored (no custom width)')
else:
    errors.append('FAIL: base .user-pill CSS not found')

# 3. Clean up the !important overrides in the media query — they conflict now.
OLD_MQ = (
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
NEW_MQ = (
    '@media (max-width: 900px) {\n'
    '        .nav-user-pill .user-pill-name {\n'
    '          display: none;\n'
    '        }\n'
    '      }'
)
if OLD_MQ in content:
    content = content.replace(OLD_MQ, NEW_MQ, 1)
    print('OK: media query cleaned up')
else:
    errors.append('FAIL: media query not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
