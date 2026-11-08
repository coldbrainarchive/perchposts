#!/usr/bin/env python3
"""Patch v270 -> v271: emoji picker input inline beside React button (no separate row wrapper)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v270.js'
dst = '_deploy/assets/index-DUcNPOLc-v271.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the chat-emoji-picker-row wrapper div with a bare inline input
# so it sits beside the React button inside the flex action sheet
OLD_PICKER = (
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
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);_setDmEmojiOpen(!1);}})})'
)
NEW_PICKER = (
    '_dmEmojiOpen&&_dmPickerId===_msg.id&&(0,L.jsx)(`input`,{className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'autoFocus:!0,'
    'onBlur:()=>_setDmEmojiOpen(!1),'
    'onChange:async _ev=>{const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);_setDmEmojiOpen(!1);}})' # } closes onChange, } closes input props, ) closes jsx call
)

if OLD_PICKER in content:
    content = content.replace(OLD_PICKER, NEW_PICKER, 1)
    print('OK: emoji input inline beside React button')
else:
    errors.append('FAIL: emoji picker row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
