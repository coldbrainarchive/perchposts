#!/usr/bin/env python3
"""Patch v542 -> v543: Bird button + overlay inside chat-msg-body children (Safari-safe)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v542.js'
dst = '_deploy/assets/index-DUcNPOLc-v543.js'

content = open(src, encoding='utf-8').read()
errors = []

OVERLAY = (
    '(0,L.jsxs)(`div`,{onClick:()=>_setBirdOpen(!1),'
    'style:{position:`fixed`,inset:0,background:`rgba(0,0,0,0.6)`,zIndex:1000,'
    'display:`flex`,alignItems:`flex-end`,justifyContent:`center`},'
    'children:[(0,L.jsxs)(`div`,{onClick:e=>e.stopPropagation(),'
    'style:{background:`#161920`,borderRadius:`18px 18px 0 0`,width:`100%`,'
    'maxWidth:`480px`,paddingBottom:32,boxShadow:`0 -8px 40px rgba(0,0,0,0.4)`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{padding:`12px 0 4px`,display:`flex`,justifyContent:`center`},'
    'children:(0,L.jsx)(`div`,{style:{width:40,height:4,borderRadius:999,background:`#374151`}})}),'
    '(0,L.jsx)(_UserCard,{username:e.username,record:e}),'
    '(0,L.jsx)(`div`,{style:{padding:`0 16px`,marginTop:8},'
    'children:(0,L.jsx)(`a`,{href:`/new?huddle=1&invite=${encodeURIComponent(e.username)}`,'
    'style:{display:`block`,textAlign:`center`,padding:`13px`,borderRadius:12,'
    'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,textDecoration:`none`},'
    'children:`Huddle`})})'
    ']})]}'
    ')'
)

# ── 1. Add _birdOpen state ────────────────────────────────────────────────────
OLD_STATE = '[b,x]=(0,_.useState)(!1),S=(0,_.useRef)(null)'
NEW_STATE = '[b,x]=(0,_.useState)(!1),[_birdOpen,_setBirdOpen]=(0,_.useState)(!1),S=(0,_.useRef)(null)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: state added')
else:
    errors.append('FAIL: state not found')

# ── 2. Bird button in action sheet ───────────────────────────────────────────
OLD_BTN = ('r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
           'onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},'
           'children:`Delete`})')
NEW_BTN = ('e.username&&!_isMe?((0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
           'onClick:()=>{y(!1);_setBirdOpen(!0)},children:`Bird`})):null,'
           'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
           'onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},'
           'children:`Delete`})')
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: Bird button added')
else:
    errors.append('FAIL: Delete button not found')

# ── 3. Add overlay inside chat-msg-body children (after emoji picker, before ]) ─
# The emoji picker is the last element; its trailing comma + ] closes body children.
# We add the overlay (using ternary for Safari) before the ].
OLD_BODY_CLOSE = ('onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},'
                  'children:`✕`})]}),]')
NEW_BODY_CLOSE = ('onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},'
                  'children:`✕`})]}),_birdOpen?' + OVERLAY + ':null,]')
if OLD_BODY_CLOSE in content:
    content = content.replace(OLD_BODY_CLOSE, NEW_BODY_CLOSE, 1)
    print('OK: overlay added inside chat-msg-body children')
else:
    errors.append('FAIL: body children close not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
