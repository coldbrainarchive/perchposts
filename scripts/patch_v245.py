#!/usr/bin/env python3
"""Patch v244 -> v245: DM compose — use chat-input-bubble classes (fixes mobile zoom, matches comment UI)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v244.js'
dst = '_deploy/assets/index-DUcNPOLc-v245.js'

content = open(src, encoding='utf-8').read()
errors = []

# The shared send logic (used in both onKeyDown and onClick)
SEND_LOGIC = (
    '_setDmSending(!0);'
    'await fetch(`${R}/send-dm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({to_username:_dmThread,content:_dmInput.trim()})});'
    '_setDmInput(``);'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
    '_setDmSending(!1);'
)

OLD_COMPOSE = (
    'display:`flex`,gap:8,padding:`10px 14px`,borderTop:`1px solid #2e303a`},'
    'children:[(0,L.jsx)(`input`,{value:_dmInput,onChange:ev=>_setDmInput(ev.target.value),'
    'onKeyDown:async ev=>{if(ev.key===`Enter`&&!ev.shiftKey&&_dmInput.trim()&&!_dmSending){'
    'ev.preventDefault();' + SEND_LOGIC +
    '}},placeholder:`Message ${_dmThread}…`,'
    'style:{flex:1,background:`#1e2530`,border:`1px solid #374151`,borderRadius:10,'
    'padding:`8px 12px`,color:`#f8fafc`,fontSize:13,outline:`none`}}),'
    '(0,L.jsx)(`button`,{disabled:_dmSending||!_dmInput.trim(),'
    'onClick:async()=>{if(!_dmInput.trim()||_dmSending)return;' + SEND_LOGIC +
    '},style:{padding:`8px 14px`,borderRadius:10,border:`none`,background:`#c084fc`,'
    'color:`#14081d`,fontWeight:700,fontSize:13,cursor:`pointer`,opacity:_dmSending?0.6:1},'
    'children:`Send`})]}'
)

NEW_COMPOSE = (
    'className:`chat-input-row`,style:{padding:`10px 14px`,borderTop:`1px solid #2e303a`},'
    'children:[(0,L.jsx)(`div`,{className:`chat-input-bubble`,'
    'children:(0,L.jsx)(`textarea`,{className:`chat-input`,value:_dmInput,'
    'onChange:ev=>_setDmInput(ev.target.value),rows:1,'
    'onKeyDown:async ev=>{if(ev.key===`Enter`&&!ev.shiftKey&&_dmInput.trim()&&!_dmSending){'
    'ev.preventDefault();' + SEND_LOGIC +
    '}},placeholder:`Message ${_dmThread}…`})}),'
    '(0,L.jsx)(`button`,{className:`chat-send-btn`,disabled:_dmSending||!_dmInput.trim(),'
    'onClick:async()=>{if(!_dmInput.trim()||_dmSending)return;' + SEND_LOGIC +
    '},children:`↑`})]}'
)

if OLD_COMPOSE in content:
    content = content.replace(OLD_COMPOSE, NEW_COMPOSE, 1)
    print('OK: DM compose replaced with chat-input-bubble style')
else:
    errors.append('FAIL: DM compose block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

opens_p = content.count('(')
closes_p = content.count(')')
print(f'Parens: {opens_p-closes_p}, Braces: {content.count("{")-content.count("}")}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
