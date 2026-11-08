#!/usr/bin/env python3
"""Patch v176 -> v177: replace emoji composite with admin-bird.png for admin."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v176.js'
dst = '_deploy/assets/index-DUcNPOLc-v177.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Jn: return simple sentinel for admin (no emoji, use img instead) ───────
OLD_JN_ADMIN = 'if(e.is_admin)return{e:`\U0001f426`,f:``,s:null,hat:!0};'
NEW_JN_ADMIN = 'if(e.is_admin)return{e:null,f:``,s:null,hat:!0};'
if OLD_JN_ADMIN in content:
    content = content.replace(OLD_JN_ADMIN, NEW_JN_ADMIN, 1)
    print('OK: Jn admin returns hat sentinel')
else:
    errors.append('FAIL: Jn admin return not found')

# ── 2. Pill badge: replace hat composite with img when i.hat ─────────────────
# Currently: emoji span + hat overlay spans
# New: single img tag sized to match the pill emoji
OLD_BADGE_CHILDREN = (
    'children:[(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[]),'
    'typeof i===`object`&&i.hat?'
    '(0,L.jsx)(`span`,{style:{position:`absolute`,bottom:`75%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`1.1em`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`})'
    ':null]}'
)
NEW_BADGE_CHILDREN = (
    'children:[typeof i===`object`&&i.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'width:`1.6em`,height:`1.6em`,objectFit:`contain`,display:`block`,margin:`auto`}})'
    ':'
    '(0,L.jsxs)(L.Fragment,{children:['
    '(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[])'
    ']})]}'
)
if OLD_BADGE_CHILDREN in content:
    content = content.replace(OLD_BADGE_CHILDREN, NEW_BADGE_CHILDREN, 1)
    print('OK: pill badge uses admin-bird.png')
else:
    errors.append('FAIL: badge children not found')

# ── 3. Header bird: replace hat composite with img ────────────────────────────
OLD_HDR_BIRD = (
    '_bird&&_bird.hat?'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,lineHeight:1},children:['
    '(0,L.jsx)(`span`,{style:{fontSize:`56px`,display:`block`},children:`\U0001f426`}),'
    '(0,L.jsx)(`span`,{style:{position:`absolute`,bottom:`75%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`46px`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`})'
    ']})'
    ':'
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1,'
    'filter:_bird&&_bird.f?_bird.f:``,display:`block`},'
    'children:_bird&&_bird.e?_bird.e:`\U0001f424`})'
)
NEW_HDR_BIRD = (
    '_bird&&_bird.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'width:`72px`,height:`72px`,objectFit:`contain`,display:`block`}})'
    ':'
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1,'
    'filter:_bird&&_bird.f?_bird.f:``,display:`block`},'
    'children:_bird&&_bird.e?_bird.e:`\U0001f424`})'
)
if OLD_HDR_BIRD in content:
    content = content.replace(OLD_HDR_BIRD, NEW_HDR_BIRD, 1)
    print('OK: header bird uses admin-bird.png')
else:
    errors.append('FAIL: header bird composite not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
