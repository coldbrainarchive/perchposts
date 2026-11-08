#!/usr/bin/env python3
"""Patch v271 -> v272: fix WebKit syntax error — replace && conditional input with always-rendered
div (display:none toggle), matching the Rr pattern. Div is a flex item inside the action sheet
so it appears inline beside the React button."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v271.js'
dst = '_deploy/assets/index-DUcNPOLc-v272.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the && short-circuit conditional input (WebKit-unsafe) with an always-rendered
# div that uses display:none/'' toggle — identical to how Rr does the emoji picker row.
OLD = (
    '_dmEmojiOpen&&_dmPickerId===_msg.id&&(0,L.jsx)(`input`,{className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'autoFocus:!0,'
    'onBlur:()=>_setDmEmojiOpen(!1),'
    'onChange:async _ev=>{const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);_setDmPickerId(null);_setDmEmojiOpen(!1);}})' # } onChange, } input props, ) jsx
)
NEW = (
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

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: && conditional replaced with always-rendered div (display toggle)')
else:
    errors.append('FAIL: conditional input not found')
    # Debug: show what's around the action sheet area
    idx = content.find('_dmEmojiOpen&&_dmPickerId===_msg.id&&', 385000)
    if idx != -1:
        print('DEBUG:', repr(content[idx:idx+120]))

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
