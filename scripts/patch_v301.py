#!/usr/bin/env python3
"""Patch v300 -> v301:
1. DM thread becomes full-screen on mobile (separate page feel, no bleed-through)
2. Quote/reply bar: full purple background, no left-border-only styling
3. Reactions back inside the bubble (above actions)"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v300.js'
dst = '_deploy/assets/index-DUcNPOLc-v301.js'

content = open(src, encoding='utf-8').read()
errors = []

REACTIONS_CODE = (
    '_rxEntries.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,children:_rxEntries.map(([_em,_us])=>(0,L.jsxs)(`button`,{type:`button`,'
    'className:`chat-reaction-pill${_us.includes(_myUser)?` mine`:``}`,onClick:async()=>{await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({message_id:_msg.id,emoji:_em})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);},children:[_em,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:_us.length})]},_em))})'
)

# ── 1. Full-screen panel when DM thread is open ───────────────────────────────
OLD_PANEL = (
    'position:`fixed`,top:0,right:0,height:`100dvh`,width:`min(420px, 100vw)`,'
    'background:`linear-gradient(180deg, #1b1d24 0%, #14161c 100%)`,borderLeft:`1px solid #2e303a`,'
    'zIndex:51,display:`flex`,flexDirection:`column`,boxShadow:`-20px 0 60px rgba(0,0,0,0.5)`'
)
NEW_PANEL = (
    '...(c===`inbox`&&_dmThread'
    '?{position:`fixed`,top:0,left:0,right:0,bottom:0,width:`100vw`,height:`100dvh`,'
    'background:`#13151c`,zIndex:200,display:`flex`,flexDirection:`column`}'
    ':{position:`fixed`,top:0,right:0,height:`100dvh`,width:`min(420px, 100vw)`,'
    'background:`linear-gradient(180deg, #1b1d24 0%, #14161c 100%)`,borderLeft:`1px solid #2e303a`,'
    'zIndex:51,display:`flex`,flexDirection:`column`,boxShadow:`-20px 0 60px rgba(0,0,0,0.5)`})'
)
if OLD_PANEL in content:
    content = content.replace(OLD_PANEL, NEW_PANEL, 1)
    print('OK: panel goes full-screen when DM thread is open')
else:
    errors.append('FAIL: panel style not found')

# ── 2. Quote bar: full purple background, no left border ─────────────────────
OLD_QUOTE_CSS = (
    '.chat-quote-bar {\n        border-left: 2px solid #c084fc;\n'
    '        padding: 6px 12px;\n        margin-bottom: 0;\n        border-radius: 0;\n'
    '        background: rgba(192,132,252,0.1);\n        border-bottom: 1px solid rgba(192,132,252,0.15);\n      }'
)
NEW_QUOTE_CSS = (
    '.chat-quote-bar {\n'
    '        padding: 6px 12px;\n        margin-bottom: 0;\n        border-radius: 0;\n'
    '        background: rgba(192,132,252,0.22);\n        border-bottom: 1px solid rgba(192,132,252,0.18);\n      }'
)
if OLD_QUOTE_CSS in content:
    content = content.replace(OLD_QUOTE_CSS, NEW_QUOTE_CSS, 1)
    print('OK: quote bar is now full purple background')
else:
    errors.append('FAIL: .chat-quote-bar CSS not found')

# ── 3a. Remove reactions from outside bubble (before ts) ─────────────────────
OLD_RX_OUTSIDE = ']}),' + REACTIONS_CODE + ',(0,L.jsx)(`span`,{className:`chat-ts`'
NEW_RX_OUTSIDE = ']}),' + '(0,L.jsx)(`span`,{className:`chat-ts`'
if OLD_RX_OUTSIDE in content:
    content = content.replace(OLD_RX_OUTSIDE, NEW_RX_OUTSIDE, 1)
    print('OK: reactions removed from outside bubble')
else:
    errors.append('FAIL: reactions-outside-bubble sequence not found')

# ── 3b. Add reactions inside bubble (after content-span, before actions) ──────
OLD_RX_POSITION = 'children:_msg.content}),_showActions&&(0,L.jsxs)(`div`,{className:`chat-action-s'
NEW_RX_POSITION = 'children:_msg.content}),' + REACTIONS_CODE + ',_showActions&&(0,L.jsxs)(`div`,{className:`chat-action-s'
if OLD_RX_POSITION in content:
    content = content.replace(OLD_RX_POSITION, NEW_RX_POSITION, 1)
    print('OK: reactions moved back inside bubble (before actions)')
else:
    errors.append('FAIL: content-span-to-actions sequence not found')

# ── 4. Reactions CSS: padding for inside-bubble use ──────────────────────────
OLD_RX_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 3px 2px;\n      }'
)
NEW_RX_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 4px 10px 6px;\n      }'
)
if OLD_RX_CSS in content:
    content = content.replace(OLD_RX_CSS, NEW_RX_CSS, 1)
    print('OK: .chat-reactions padding restored for inside-bubble')
else:
    errors.append('FAIL: .chat-reactions CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
