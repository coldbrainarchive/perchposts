#!/usr/bin/env python3
"""Patch v269 -> v270: React button opens emoji picker row; reply-to uses purple accent."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v269.js'
dst = '_deploy/assets/index-DUcNPOLc-v270.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _dmEmojiOpen state next to _dmPickerId ─────────────────────────────
OLD_PICKER_STATE = '[_dmPickerId,_setDmPickerId]=(0,_.useState)(null),'
NEW_PICKER_STATE = '[_dmPickerId,_setDmPickerId]=(0,_.useState)(null),[_dmEmojiOpen,_setDmEmojiOpen]=(0,_.useState)(!1),'
if OLD_PICKER_STATE in content:
    content = content.replace(OLD_PICKER_STATE, NEW_PICKER_STATE, 1)
    print('OK: _dmEmojiOpen state added')
else:
    errors.append('FAIL: _dmPickerId state not found')

# ── 2. Replace DM action sheet: React button + inline input → picker row ──────
OLD_ACTION = (
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{let _inp=document.getElementById(`dm-emoji-${_msg.id}`);'
    'if(_inp){_inp.value=``;_inp.style.display=_inp.style.display===`none`?``:``; _inp.focus();}},children:`React`}),'
    '(0,L.jsx)(`input`,{id:`dm-emoji-${_msg.id}`,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:async _ev=>{const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);}})'
)
NEW_ACTION = (
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{_setDmEmojiOpen(!0);},children:`React`}),'
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`,'
    'style:{display:_dmEmojiOpen&&_dmPickerId===_msg.id?``:`none`},'
    'children:(0,L.jsx)(`input`,{className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onBlur:()=>_setDmEmojiOpen(!1),'
    'onChange:async _ev=>{const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);_setDmEmojiOpen(!1);}})}'
    ')'
)

if OLD_ACTION in content:
    content = content.replace(OLD_ACTION, NEW_ACTION, 1)
    print('OK: React button uses emoji picker row')
else:
    errors.append('FAIL: DM action sheet emoji input not found')

# ── 3. Reply-to quote: purple left border + purple sender name ────────────────
OLD_REPLY_QUOTE = (
    '_msg.reply_to&&(0,L.jsxs)(`div`,{style:{background:`rgba(148,163,184,0.08)`,'
    'borderLeft:`2px solid rgba(148,163,184,0.4)`,padding:`4px 10px`,fontSize:11,'
    'color:`#64748b`,display:`flex`,gap:4,alignItems:`center`,overflow:`hidden`},'
    'children:[(0,L.jsx)(`span`,{style:{fontWeight:700,flexShrink:0},'
    'children:_msg.reply_to.from_username})'
)
NEW_REPLY_QUOTE = (
    '_msg.reply_to&&(0,L.jsxs)(`div`,{style:{background:`rgba(192,132,252,0.08)`,'
    'borderLeft:`2px solid #c084fc`,padding:`4px 10px`,fontSize:11,'
    'color:`#94a3b8`,display:`flex`,gap:4,alignItems:`center`,overflow:`hidden`},'
    'children:[(0,L.jsx)(`span`,{style:{fontWeight:700,flexShrink:0,color:`#c084fc`},'
    'children:_msg.reply_to.from_username})'
)
if OLD_REPLY_QUOTE in content:
    content = content.replace(OLD_REPLY_QUOTE, NEW_REPLY_QUOTE, 1)
    print('OK: reply-to quote uses purple accent')
else:
    errors.append('FAIL: reply-to quote not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
