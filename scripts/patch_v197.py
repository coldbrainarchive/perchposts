#!/usr/bin/env python3
"""Patch v196 -> v197: revert home-shell padding; add top margin only on post view."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v196.js'
dst = '_deploy/assets/index-DUcNPOLc-v197.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Revert home-shell top padding (affected feed too) ─────────────────────
OLD_PADDING = (
    '.home-shell {\n'
    '        display: block;\n'
    '        width: min(1280px, 100%);\n'
    '        margin: 0 auto;\n'
    '        padding: 18px 20px 32px;\n'
    '        box-sizing: border-box;\n'
    '      }'
)
NEW_PADDING = (
    '.home-shell {\n'
    '        display: block;\n'
    '        width: min(1280px, 100%);\n'
    '        margin: 0 auto;\n'
    '        padding: 0 20px 32px;\n'
    '        box-sizing: border-box;\n'
    '      }'
)
if OLD_PADDING in content:
    content = content.replace(OLD_PADDING, NEW_PADDING, 1)
    print('OK: home-shell padding reverted')
else:
    errors.append('FAIL: home-shell CSS not found')

# ── 2. Add top margin only to the post view main element (unique to Wr) ──────
# The post view (Wr) returns: de.filter(...), (0,L.jsxs)(`div`,{home-shell,...
# Its main has style:{textAlign:`left`} — unique to Wr in this context.
OLD_MAIN = (
    'return de.filter(e=>!e.parent_comment_id),(0,L.jsxs)(`div`,{className:`home-shell`,'
    'children:[(0,L.jsx)(Lr,{}),(0,L.jsxs)(`main`,{className:`home-feed`,'
    'style:{textAlign:`left`},'
)
NEW_MAIN = (
    'return de.filter(e=>!e.parent_comment_id),(0,L.jsxs)(`div`,{className:`home-shell`,'
    'children:[(0,L.jsx)(Lr,{}),(0,L.jsxs)(`main`,{className:`home-feed`,'
    'style:{textAlign:`left`,marginTop:18},'
)
if OLD_MAIN in content:
    content = content.replace(OLD_MAIN, NEW_MAIN, 1)
    print('OK: marginTop:18 added to post view main')
else:
    errors.append('FAIL: post view main not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
