#!/usr/bin/env python3
"""Patch v187 -> v188: shrink card proportions; fit-content width; smaller admin bird."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v187.js'
dst = '_deploy/assets/index-DUcNPOLc-v188.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. .chat-msg — fit-content width so card only as wide as its text ─────────
OLD_MSG = (
    '.chat-msg {\n'
    '        display: block;\n'
    '        max-width: 80%;\n'
    '        margin-bottom: 10px;\n'
    '      }'
)
NEW_MSG = (
    '.chat-msg {\n'
    '        display: inline-block;\n'
    '        width: fit-content;\n'
    '        max-width: min(80%, 520px);\n'
    '        margin-bottom: 10px;\n'
    '        vertical-align: top;\n'
    '      }'
)
if OLD_MSG in content:
    content = content.replace(OLD_MSG, NEW_MSG, 1)
    print('OK: .chat-msg fit-content width')
else:
    errors.append('FAIL: .chat-msg CSS not found')

# ── 2. .chat-msg-body — ensure it fills the inline-block card width ───────────
OLD_BODY = (
    '.chat-msg-body {\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        border-radius: 18px;\n'
    '        overflow: hidden;\n'
    '      }'
)
NEW_BODY = (
    '.chat-msg-body {\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        border-radius: 18px;\n'
    '        overflow: hidden;\n'
    '        width: 100%;\n'
    '      }'
)
if OLD_BODY in content:
    content = content.replace(OLD_BODY, NEW_BODY, 1)
    print('OK: .chat-msg-body width')
else:
    errors.append('FAIL: .chat-msg-body CSS not found')

# ── 3. Header padding smaller ─────────────────────────────────────────────────
OLD_META = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 10px;\n'
    '        padding: 10px 14px;\n'
    '      }'
)
NEW_META = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 8px;\n'
    '        padding: 7px 12px;\n'
    '      }'
)
if OLD_META in content:
    content = content.replace(OLD_META, NEW_META, 1)
    print('OK: .chat-msg-meta padding')
else:
    errors.append('FAIL: .chat-msg-meta CSS not found')

# ── 4. Admin bird: shrink container and image to match emoji size ─────────────
OLD_ADMIN = (
    'style:{position:`relative`,display:`inline-block`,width:`32px`,height:`32px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`52px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
NEW_ADMIN = (
    'style:{position:`relative`,display:`inline-block`,width:`22px`,height:`22px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`36px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
if OLD_ADMIN in content:
    content = content.replace(OLD_ADMIN, NEW_ADMIN, 1)
    print('OK: admin bird size reduced')
else:
    errors.append('FAIL: admin bird container not found')

# ── 5. Regular bird emoji: 32 → 22px ─────────────────────────────────────────
OLD_BIRD = (
    ':(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'fontSize:32,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,32):[])]}),'
)
NEW_BIRD = (
    ':(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'fontSize:22,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,22):[])]}),'
)
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: regular bird emoji size reduced')
else:
    errors.append('FAIL: regular bird span not found')

# ── 6. Username font: 15 → 13px ───────────────────────────────────────────────
OLD_UNAME = 'style:{fontWeight:700,fontSize:15,color:`#0a0a0a`,flex:1,minWidth:0}'
NEW_UNAME = 'style:{fontWeight:700,fontSize:13,color:`#0a0a0a`,flex:1,minWidth:0}'
if OLD_UNAME in content:
    content = content.replace(OLD_UNAME, NEW_UNAME, 1)
    print('OK: username font size reduced')
else:
    errors.append('FAIL: username style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
