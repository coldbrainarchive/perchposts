#!/usr/bin/env python3
"""Patch v544 -> v545:
- Replace drag handle with "Tap to close" text at top
- Remove stopPropagation so tapping anywhere closes
- Rename Huddle button to See Posts, navigate to /?user=username
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v544.js'
dst = '_deploy/assets/index-DUcNPOLc-v545.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove stopPropagation + replace drag handle with tap-to-close ─────────
OLD_CARD_TOP = ('(0,L.jsxs)(`div`,{onClick:e=>e.stopPropagation(),'
                'style:{background:`#161920`,borderRadius:`18px 18px 0 0`,width:`100%`,'
                'maxWidth:`480px`,paddingBottom:32,boxShadow:`0 -8px 40px rgba(0,0,0,0.4)`},'
                'children:[(0,L.jsx)(`div`,{style:{padding:`12px 0 4px`,display:`flex`,'
                'justifyContent:`center`},children:(0,L.jsx)(`div`,{style:{width:40,height:4,'
                'borderRadius:999,background:`#374151`}})}),')
NEW_CARD_TOP = ('(0,L.jsxs)(`div`,{'
                'style:{background:`#161920`,borderRadius:`18px 18px 0 0`,width:`100%`,'
                'maxWidth:`480px`,paddingBottom:32,boxShadow:`0 -8px 40px rgba(0,0,0,0.4)`},'
                'children:[(0,L.jsx)(`div`,{style:{padding:`10px 16px 4px`,display:`flex`,'
                'justifyContent:`flex-end`},'
                'children:(0,L.jsx)(`button`,{onClick:()=>_setBirdOpen(!1),'
                'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,'
                'fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`})}),')
if OLD_CARD_TOP in content:
    content = content.replace(OLD_CARD_TOP, NEW_CARD_TOP, 1)
    print('OK: drag handle → tap to close, stopPropagation removed')
else:
    errors.append('FAIL: card top not found')

# ── 2. See Posts button (was Huddle, navigates to /?user=username) ────────────
OLD_BTN = ('children:(0,L.jsx)(`a`,{href:`/new?huddle=1&invite=${encodeURIComponent(e.username)}`,'
           'style:{display:`block`,textAlign:`center`,padding:`13px`,borderRadius:12,'
           'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,textDecoration:`none`},'
           'children:`Huddle`})')
NEW_BTN = ('children:(0,L.jsx)(`a`,{href:`/?user=${encodeURIComponent(e.username)}`,'
           'style:{display:`block`,textAlign:`center`,padding:`13px`,borderRadius:12,'
           'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,textDecoration:`none`},'
           'children:`See Posts`})')
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: Huddle → See Posts button')
else:
    errors.append('FAIL: Huddle button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
