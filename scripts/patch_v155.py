#!/usr/bin/env python3
"""Patch v154 -> v155: centre badge with margin:auto — works in any flex container."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v154.js'
dst = '_deploy/assets/index-DUcNPOLc-v155.js'

content = open(src, encoding='utf-8').read()
errors = []

# margin:auto on a flex item absorbs all available free space on both sides,
# centering it unconditionally regardless of container width or justify-content.
# Add it to both the CSS class and the badge inline style.

# 1. CSS class
OLD_BADGE_CSS = (
    'user-pill-badge {\n'
    '        font-size: 12px;\n'
    '        line-height: 1;\n'
    '      }'
)
NEW_BADGE_CSS = (
    'user-pill-badge {\n'
    '        font-size: 12px;\n'
    '        line-height: 1;\n'
    '        margin: auto;\n'
    '      }'
)
if OLD_BADGE_CSS in content:
    content = content.replace(OLD_BADGE_CSS, NEW_BADGE_CSS, 1)
    print('OK: margin:auto added to .user-pill-badge CSS')
else:
    errors.append('FAIL: .user-pill-badge CSS not found')

# 2. Badge inline style
OLD_BADGE_STYLE = (
    'style:{position:`relative`,display:`inline-block`,'
    'width:`1.1em`,height:`1.1em`,lineHeight:1,verticalAlign:`middle`}'
)
NEW_BADGE_STYLE = (
    'style:{position:`relative`,display:`inline-block`,'
    'width:`1.1em`,height:`1.1em`,lineHeight:1,verticalAlign:`middle`,margin:`auto`}'
)
if OLD_BADGE_STYLE in content:
    content = content.replace(OLD_BADGE_STYLE, NEW_BADGE_STYLE, 1)
    print('OK: margin:auto added to badge inline style')
else:
    errors.append('FAIL: badge inline style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
