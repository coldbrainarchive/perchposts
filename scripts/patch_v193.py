#!/usr/bin/env python3
"""Patch v192 -> v193: fix admin bird alignment; truncate long usernames."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v192.js'
dst = '_deploy/assets/index-DUcNPOLc-v193.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Admin bird — drop absolute positioning, just use inline img at 17px ───
# The absolute+overflow approach shifts the image left of its container,
# making it look closer to the edge than the regular emoji.
OLD_ADMIN = (
    '_bd&&_bd.hat'
    '?(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,width:`17px`,height:`17px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`26px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]})'
)
NEW_ADMIN = (
    '_bd&&_bd.hat'
    '?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{height:`17px`,width:`auto`,flexShrink:0,display:`block`}})'
)
if OLD_ADMIN in content:
    content = content.replace(OLD_ADMIN, NEW_ADMIN, 1)
    print('OK: admin bird → simple inline img')
else:
    errors.append('FAIL: admin bird block not found')

# ── 2. Username — no wrap, ellipsis on overflow ───────────────────────────────
OLD_UNAME = 'style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,minWidth:0}'
NEW_UNAME = 'style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,minWidth:0,whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`}'
if OLD_UNAME in content:
    content = content.replace(OLD_UNAME, NEW_UNAME, 1)
    print('OK: username truncates instead of wrapping')
else:
    errors.append('FAIL: username style not found')

# ── 3. Header row — never wrap ────────────────────────────────────────────────
OLD_META_CSS = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        padding: 5px 10px;\n'
    '      }'
)
NEW_META_CSS = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        padding: 5px 10px;\n'
    '        overflow: hidden;\n'
    '      }'
)
if OLD_META_CSS in content:
    content = content.replace(OLD_META_CSS, NEW_META_CSS, 1)
    print('OK: header overflow hidden')
else:
    errors.append('FAIL: .chat-msg-meta CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
