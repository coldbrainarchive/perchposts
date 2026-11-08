#!/usr/bin/env python3
"""Patch v559 -> v560:
When postcard tags overflow one line, collapse the last tag to emoji-only.
- Change feed-post-board-group from flex-wrap:wrap to nowrap + overflow:hidden
- Add :last-child rule: flex-shrink:1!important + overflow:hidden + min-width:22px
  so the last chip shrinks to emoji-width, hiding its text label
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v559.js'
dst = '_deploy/assets/index-DUcNPOLc-v560.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_CSS = (
    '.feed-post-board-group {\n'
    '        display: inline-flex;\n'
    '        align-items: center;\n'
    '        gap: 8px;\n'
    '        min-width: 0;\n'
    '        flex-wrap: wrap;\n'
    '      }'
)
NEW_CSS = (
    '.feed-post-board-group {\n'
    '        display: inline-flex;\n'
    '        align-items: center;\n'
    '        gap: 8px;\n'
    '        min-width: 0;\n'
    '        flex-wrap: nowrap;\n'
    '        overflow: hidden;\n'
    '      }\n'
    '      .feed-post-board-group > :last-child {\n'
    '        flex-shrink: 1!important;\n'
    '        overflow: hidden;\n'
    '        min-width: 22px;\n'
    '      }'
)

count = content.count(OLD_CSS)
if count == 2:
    content = content.replace(OLD_CSS, NEW_CSS)
    print(f'OK: updated {count} instances of feed-post-board-group CSS')
elif count == 1:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: updated 1 instance of feed-post-board-group CSS')
else:
    errors.append(f'FAIL: feed-post-board-group CSS not found (found {count})')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
