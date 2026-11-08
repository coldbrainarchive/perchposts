#!/usr/bin/env python3
"""Patch v189 -> v190: smaller comment bubbles and username."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v189.js'
dst = '_deploy/assets/index-DUcNPOLc-v190.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Header padding ─────────────────────────────────────────────────────────
OLD_META = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 8px;\n'
    '        padding: 7px 12px;\n'
    '      }'
)
NEW_META = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        padding: 5px 10px;\n'
    '      }'
)
if OLD_META in content:
    content = content.replace(OLD_META, NEW_META, 1)
    print('OK: header padding reduced')
else:
    errors.append('FAIL: .chat-msg-meta CSS not found')

# ── 2. Bubble body padding ────────────────────────────────────────────────────
OLD_BUBBLE = 'padding: 9px 13px;'
NEW_BUBBLE = 'padding: 6px 10px;'
if OLD_BUBBLE in content:
    content = content.replace(OLD_BUBBLE, NEW_BUBBLE, 1)
    print('OK: bubble padding reduced')
else:
    errors.append('FAIL: bubble padding not found')

# ── 3. Username font size: 13 → 11px ─────────────────────────────────────────
OLD_UNAME = 'style:{fontWeight:700,fontSize:13,color:`#0a0a0a`,flex:1,minWidth:0}'
NEW_UNAME = 'style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,minWidth:0}'
if OLD_UNAME in content:
    content = content.replace(OLD_UNAME, NEW_UNAME, 1)
    print('OK: username font reduced to 11px')
else:
    errors.append('FAIL: username style not found')

# ── 4. Bird emoji: 22 → 17px ─────────────────────────────────────────────────
OLD_BIRD = (
    ':(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'fontSize:22,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,22):[])]}),'
)
NEW_BIRD = (
    ':(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'fontSize:17,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,17):[])]}),'
)
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: bird emoji reduced to 17px')
else:
    errors.append('FAIL: bird emoji span not found')

# ── 5. Admin bird: 18/28 → 14/22px ───────────────────────────────────────────
OLD_ADMIN = (
    'style:{position:`relative`,display:`inline-block`,width:`18px`,height:`18px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`28px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
NEW_ADMIN = (
    'style:{position:`relative`,display:`inline-block`,width:`14px`,height:`14px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`22px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
if OLD_ADMIN in content:
    content = content.replace(OLD_ADMIN, NEW_ADMIN, 1)
    print('OK: admin bird reduced to 22px')
else:
    errors.append('FAIL: admin bird not found')

# ── 6. Bubble font size: keep 14px but reduce line-height ────────────────────
OLD_FONT = 'font-size: 14px;\n        line-height: 1.45;'
NEW_FONT = 'font-size: 13px;\n        line-height: 1.4;'
if OLD_FONT in content:
    content = content.replace(OLD_FONT, NEW_FONT, 1)
    print('OK: bubble font reduced to 13px')
else:
    errors.append('FAIL: bubble font-size not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
