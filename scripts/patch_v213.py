#!/usr/bin/env python3
"""Patch v212 -> v213: remove back arrows from post page; add swipe-from-left-edge to go back."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v212.js'
dst = '_deploy/assets/index-DUcNPOLc-v213.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove back arrow from the post-view board-group ──────────────────────
OLD_ARROW1 = (
    'feed-post-board-group`,style:{flexWrap:`wrap`,gap:5},children:['
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>o(-1),'
    'style:{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
    'width:22,height:22,borderRadius:999,border:`1px solid #323b48`,'
    'background:`#1d242d`,color:`#dbe4ee`,fontSize:11,fontWeight:800,'
    'cursor:`pointer`,flexShrink:0,boxSizing:`border-box`},children:`←`}),'
)
NEW_ARROW1 = (
    'feed-post-board-group`,style:{flexWrap:`wrap`,gap:5},children:['
)
if OLD_ARROW1 in content:
    content = content.replace(OLD_ARROW1, NEW_ARROW1, 1)
    print('OK: removed back arrow from post-view board-group')
else:
    errors.append('FAIL: board-group back arrow not found')

# ── 2. Remove back arrow from chat-panel-header ───────────────────────────────
OLD_ARROW2 = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},children:['
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>o(-1),'
    'style:{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
    'width:26,height:26,borderRadius:999,border:`none`,'
    'background:`#20262f`,color:`#dbe4ee`,fontSize:12,fontWeight:800,'
    'cursor:`pointer`,flexShrink:0},children:`←`}),'
    '(0,L.jsxs)(`span`,{className:`comments-panel-title`,children:[u.length,` Chats`]})'
    ']}),'
)
NEW_ARROW2 = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},children:['
    '(0,L.jsxs)(`span`,{className:`comments-panel-title`,children:[u.length,` Chats`]})'
    ']}),'
)
if OLD_ARROW2 in content:
    content = content.replace(OLD_ARROW2, NEW_ARROW2, 1)
    print('OK: removed back arrow from chat-panel-header')
else:
    errors.append('FAIL: chat-panel-header back arrow not found')

# ── 3. Inject swipe-from-left-edge useEffect into Wr ─────────────────────────
# Insert right after the scroll-to-top effect at mount
OLD_EFFECT = '(0,_.useEffect)(()=>{window.scrollTo(0,0)},[r])'
NEW_EFFECT = (
    '(0,_.useEffect)(()=>{window.scrollTo(0,0)},[r]);'
    '(0,_.useEffect)(()=>{'
    'let _sx=0,_sy=0;'
    'const _ts=e=>{_sx=e.touches[0].clientX;_sy=e.touches[0].clientY;};'
    'const _te=e=>{'
    'const _dx=e.changedTouches[0].clientX-_sx;'
    'const _dy=e.changedTouches[0].clientY-_sy;'
    'if(_sx<50&&_dx>60&&Math.abs(_dx)>Math.abs(_dy)*1.5)o(-1);'
    '};'
    'document.addEventListener(`touchstart`,_ts,{passive:!0});'
    'document.addEventListener(`touchend`,_te,{passive:!0});'
    'return()=>{document.removeEventListener(`touchstart`,_ts);'
    'document.removeEventListener(`touchend`,_te);};'
    '},[r])'
)
if OLD_EFFECT in content:
    content = content.replace(OLD_EFFECT, NEW_EFFECT, 1)
    print('OK: swipe-back gesture added')
else:
    errors.append('FAIL: scroll-to-top effect not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
