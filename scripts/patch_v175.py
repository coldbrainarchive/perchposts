#!/usr/bin/env python3
"""Patch v174 -> v175: admin gets bird+top-hat composite logo."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v174.js'
dst = '_deploy/assets/index-DUcNPOLc-v175.js'

content = open(src, encoding='utf-8').read()
errors = []

HAT_SPAN_PILL = (
    '(0,L.jsx)(`span`,{style:{position:`absolute`,top:`-55%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`1em`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`})'
)

# ── 1. Return admin hat-bird from Jn ─────────────────────────────────────────
OLD_JN_START = (
    'function Jn(e){if(!e)return null;'
    'if(e.username&&_jailed.has(e.username))return`\U0001fab9`;'
    'if(e.username&&_banned.has(e.username))return`❌`;'
    'if(e.browser_id&&String(e.browser_id).startsWith(`bot-`))return`\U0001f916`;'
    'var _s'
)
NEW_JN_START = (
    'function Jn(e){if(!e)return null;'
    'if(e.username&&_jailed.has(e.username))return`\U0001fab9`;'
    'if(e.username&&_banned.has(e.username))return`❌`;'
    'if(e.browser_id&&String(e.browser_id).startsWith(`bot-`))return`\U0001f916`;'
    'if(e.is_admin)return{e:`\U0001f426`,f:``,s:null,hat:!0};'
    'var _s'
)
if OLD_JN_START in content:
    content = content.replace(OLD_JN_START, NEW_JN_START, 1)
    print('OK: admin returns hat-bird object from Jn')
else:
    errors.append('FAIL: Jn start not found')

# ── 2. Add hat overlay to badge render (pill) ────────────────────────────────
OLD_BADGE_CHILDREN = (
    'children:[(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[])]}'
)
NEW_BADGE_CHILDREN = (
    'children:[(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[]),'
    'typeof i===`object`&&i.hat?' + HAT_SPAN_PILL + ':null]}'
)
if OLD_BADGE_CHILDREN in content:
    content = content.replace(OLD_BADGE_CHILDREN, NEW_BADGE_CHILDREN, 1)
    print('OK: hat overlay added to pill badge')
else:
    errors.append('FAIL: badge children not found')

# ── 3. Add hat overlay to header bird (large 56px) ───────────────────────────
OLD_HDR_BIRD = (
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1,'
    'filter:_bird&&_bird.f?_bird.f:``,display:`block`},'
    'children:_bird&&_bird.e?_bird.e:`\U0001f424`})'
)
NEW_HDR_BIRD = (
    '_bird&&_bird.hat?'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,lineHeight:1},children:['
    '(0,L.jsx)(`span`,{style:{fontSize:`56px`,display:`block`},children:`\U0001f426`}),'
    '(0,L.jsx)(`span`,{style:{position:`absolute`,top:`-55%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`44px`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`})'
    ']})'
    ':'
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1,'
    'filter:_bird&&_bird.f?_bird.f:``,display:`block`},'
    'children:_bird&&_bird.e?_bird.e:`\U0001f424`})'
)
if OLD_HDR_BIRD in content:
    content = content.replace(OLD_HDR_BIRD, NEW_HDR_BIRD, 1)
    print('OK: hat overlay added to header bird')
else:
    errors.append('FAIL: header bird not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
