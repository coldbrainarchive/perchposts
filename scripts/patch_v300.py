#!/usr/bin/env python3
"""Patch v299 -> v300: DM UX fixes.
1. Scroll to bottom on load (add ref + scrollTop=scrollHeight after fetch)
2. Prevent iOS zoom on compose tap (font-size 16px)
3. Move reactions OUTSIDE the bubble (float below, iMessage style)
4. Fix panel height for iOS keyboard (100dvh instead of bottom:0)
5. Compose: cleaner border/background"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v299.js'
dst = '_deploy/assets/index-DUcNPOLc-v300.js'

content = open(src, encoding='utf-8').read()
errors = []

REACTIONS_CODE = (
    '_rxEntries.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,children:_rxEntries.map(([_em,_us])=>(0,L.jsxs)(`button`,{type:`button`,'
    'className:`chat-reaction-pill${_us.includes(_myUser)?` mine`:``}`,onClick:async()=>{await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({message_id:_msg.id,emoji:_em})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);},children:[_em,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:_us.length})]},_em))})'
)

# ── 1. Add _dmWRef useRef ─────────────────────────────────────────────────────
OLD_REF = 'ae=(0,_.useRef)({startX:0,startY:0});let _rank'
NEW_REF = 'ae=(0,_.useRef)({startX:0,startY:0});let _dmWRef=(0,_.useRef)(null);let _rank'
if OLD_REF in content:
    content = content.replace(OLD_REF, NEW_REF, 1)
    print('OK: _dmWRef ref added')
else:
    errors.append('FAIL: ae useRef not found')

# ── 2. Attach ref to DM chat-window ──────────────────────────────────────────
OLD_WIN = '(0,L.jsx)(`div`,{className:`chat-window`,children:_dmMsgs.length===0'
NEW_WIN = '(0,L.jsx)(`div`,{className:`chat-window`,ref:_dmWRef,children:_dmMsgs.length===0'
if OLD_WIN in content:
    content = content.replace(OLD_WIN, NEW_WIN, 1)
    print('OK: ref attached to DM chat-window')
else:
    errors.append('FAIL: DM chat-window not found')

# ── 3. Scroll to bottom after messages load ───────────────────────────────────
OLD_FETCH = '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
NEW_FETCH = ('let _dms2=(_r.ok?await _r.json():{}).messages||[];'
             '_setDmMsgs(_dms2);'
             'setTimeout(()=>{let _w=_dmWRef.current;if(_w)_w.scrollTop=_w.scrollHeight;},80);')
if OLD_FETCH in content:
    content = content.replace(OLD_FETCH, NEW_FETCH, 1)
    print('OK: scroll-to-bottom added after messages fetch')
else:
    errors.append('FAIL: _setDmMsgs fetch line not found')

# ── 4. Move reactions OUTSIDE bubble — remove from inside bubble children ─────
OLD_RX_INSIDE = 'children:_msg.content}),' + REACTIONS_CODE + ',_showActions'
NEW_RX_INSIDE = 'children:_msg.content}),_showActions'
if OLD_RX_INSIDE in content:
    content = content.replace(OLD_RX_INSIDE, NEW_RX_INSIDE, 1)
    print('OK: reactions removed from inside bubble children')
else:
    errors.append('FAIL: reactions-inside-bubble not found')

# ── 5. Add reactions after bubble close (before ts) ──────────────────────────
OLD_AFTER_BUBBLE = ']}),' + '(0,L.jsx)(`span`,{className:`chat-ts`,children:Un(_msg.created_at)})'
NEW_AFTER_BUBBLE = ']}),' + REACTIONS_CODE + ',(0,L.jsx)(`span`,{className:`chat-ts`,children:Un(_msg.created_at)})'
if OLD_AFTER_BUBBLE in content:
    content = content.replace(OLD_AFTER_BUBBLE, NEW_AFTER_BUBBLE, 1)
    print('OK: reactions added outside bubble before ts')
else:
    errors.append('FAIL: bubble-close+ts sequence not found')

# ── 6. Fix iOS font-size zoom (16px prevents Safari auto-zoom) ────────────────
OLD_FONT = '        font-size: 14px;\n        font-family: inherit;\n        padding: 8px 12px;\n        resize: none;\n        max-height: 100px;'
NEW_FONT = '        font-size: 16px;\n        font-family: inherit;\n        padding: 8px 12px;\n        resize: none;\n        max-height: 100px;'
if OLD_FONT in content:
    content = content.replace(OLD_FONT, NEW_FONT, 1)
    print('OK: compose font-size set to 16px (prevents iOS zoom)')
else:
    errors.append('FAIL: .chat-input font-size not found')

# ── 7. Fix panel height for iOS keyboard (dvh adjusts for keyboard) ───────────
OLD_PANEL = 'position:`fixed`,top:0,right:0,bottom:0,width:`min(420px, 100vw)`'
NEW_PANEL = 'position:`fixed`,top:0,right:0,height:`100dvh`,width:`min(420px, 100vw)`'
if OLD_PANEL in content:
    content = content.replace(OLD_PANEL, NEW_PANEL, 1)
    print('OK: panel height changed to 100dvh for iOS keyboard support')
else:
    errors.append('FAIL: panel position style not found')

# ── 8. Reactions CSS — float naturally below bubble with small gap ────────────
OLD_RX_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 4px 10px 6px;\n      }'
)
NEW_RX_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 3px 2px;\n      }'
)
if OLD_RX_CSS in content:
    content = content.replace(OLD_RX_CSS, NEW_RX_CSS, 1)
    print('OK: .chat-reactions CSS updated for outside-bubble layout')
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
