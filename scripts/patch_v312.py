#!/usr/bin/env python3
"""Patch v311 -> v312: fix comment section as a bounded viewport container.
The comments-shell should be sticky to the top and fill 100dvh so:
- chat-window gets a bounded height and scrolls internally
- compose sits at the bottom of the 100dvh container (always visible)
Remove the bad position:fixed compose override from v311."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v311.js'
dst = '_deploy/assets/index-DUcNPOLc-v312.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Revert the bad v311 compose fix (position:fixed + padding-bottom:80px) ─
OLD_SHELL = (
    '.comments-shell {\n        margin-top: 18px;\n        padding-bottom: 80px;\n      }\n\n'
    '      .comments-shell .chat-compose {\n'
    '        position: fixed;\n'
    '        bottom: 0;\n'
    '        left: 0;\n'
    '        right: 0;\n'
    '        z-index: 50;\n'
    '        padding-bottom: max(10px, env(safe-area-inset-bottom, 0px));\n'
    '      }'
)
NEW_SHELL = (
    # Make comments-shell a sticky full-viewport bounded container
    '.comments-shell {\n'
    '        margin-top: 18px;\n'
    '        position: sticky;\n'
    '        top: 0;\n'
    '        height: 100dvh;\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        overflow: hidden;\n'
    '      }'
)
if OLD_SHELL in content:
    content = content.replace(OLD_SHELL, NEW_SHELL, 1)
    print('OK: comments-shell is now a sticky 100dvh bounded container')
else:
    errors.append('FAIL: v311 shell CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
