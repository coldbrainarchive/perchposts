#!/usr/bin/env python3
"""Patch v272 -> v273: DM thread matches Rr comment section exactly.
- Reply-to quote uses chat-quote-bar/chat-quote-name/chat-quote-text CSS classes
- Emoji picker uses chat-emoji-picker-row CSS class (like Rr)
- Action sheet adds Find (scroll to parent) and Delete (own messages) buttons
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v272.js'
dst = '_deploy/assets/index-DUcNPOLc-v273.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace inline reply-to div with chat-quote-bar CSS classes ────────────
OLD_QUOTE = (
    '_msg.reply_to&&(0,L.jsxs)(`div`,{style:{background:`rgba(192,132,252,0.08)`,'
    'borderLeft:`2px solid #c084fc`,padding:`4px 10px`,fontSize:11,'
    'color:`#94a3b8`,display:`flex`,gap:4,alignItems:`center`,overflow:`hidden`},'
    'children:[(0,L.jsx)(`span`,{style:{fontWeight:700,flexShrink:0,color:`#c084fc`},'
    'children:_msg.reply_to.from_username}),(0,L.jsx)(`span`,{style:{overflow:`hidden`,'
    'textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:_msg.reply_to.content})]})'
)
NEW_QUOTE = (
    '_msg.reply_to&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,'
    'children:[(0,L.jsx)(`span`,{className:`chat-quote-name`,'
    'children:_msg.reply_to.from_username}),(0,L.jsx)(`p`,{className:`chat-quote-text`,'
    'children:_msg.reply_to.content})]})'
)
if OLD_QUOTE in content:
    content = content.replace(OLD_QUOTE, NEW_QUOTE, 1)
    print('OK: reply-to uses chat-quote-bar classes')
else:
    errors.append('FAIL: reply-to quote not found')

# ── 2. Replace inline div emoji wrapper with chat-emoji-picker-row class ──────
OLD_EMOJI_WRAP = (
    '(0,L.jsx)(`div`,{style:{display:_dmEmojiOpen&&_dmPickerId===_msg.id?``:`none`,padding:0},'
    'children:(0,L.jsx)(`input`,{className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onBlur:()=>_setDmEmojiOpen(!1),'
    'onChange:async _ev=>{const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);_setDmEmojiOpen(!1);}})})' # } onChange, } input props, ) input jsx, } div props, ) div jsx
)
NEW_EMOJI_WRAP = (
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`,style:{display:_dmEmojiOpen&&_dmPickerId===_msg.id?``:`none`},'
    'children:(0,L.jsx)(`input`,{className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onBlur:()=>_setDmEmojiOpen(!1),'
    'onChange:async _ev=>{const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);_setDmEmojiOpen(!1);}})})' # same closing
)
if OLD_EMOJI_WRAP in content:
    content = content.replace(OLD_EMOJI_WRAP, NEW_EMOJI_WRAP, 1)
    print('OK: emoji picker uses chat-emoji-picker-row class')
else:
    errors.append('FAIL: emoji picker wrapper not found')

# ── 3. Add Find + Delete buttons to DM action sheet ──────────────────────────
# Current action sheet ends with: React button, emoji picker div
# We add Find (scroll to parent) and Delete (own messages) before the emoji picker
OLD_REACT_BTN = (
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{_setDmEmojiOpen(!0);},children:`React`}),'
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`'
)
NEW_REACT_BTN = (
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{_setDmEmojiOpen(!0);},children:`React`}),'
    '_msg.reply_to&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{const _el=document.querySelector(`[data-comment-id="${_msg.reply_to.id}"]`);'
    '_el&&_el.scrollIntoView({behavior:`smooth`,block:`center`});_setDmPickerId(null);},children:`Find`}),'
    '_mine&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:async()=>{if(!confirm(`Delete this message?`))return;'
    'await fetch(`${R}/delete-dm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);},children:`Delete`}),'
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`'
)
if OLD_REACT_BTN in content:
    content = content.replace(OLD_REACT_BTN, NEW_REACT_BTN, 1)
    print('OK: Find + Delete buttons added to action sheet')
else:
    errors.append('FAIL: React button anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
