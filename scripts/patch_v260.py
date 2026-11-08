#!/usr/bin/env python3
"""Patch v259 -> v260: fix hooks-in-map error — use single _dmPickerId state instead."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v259.js'
dst = '_deploy/assets/index-DUcNPOLc-v260.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _dmPickerId state alongside _dmReplyTo ────────────────────────────
OLD_STATE = '[_dmReplyTo,_setDmReplyTo]=(0,_.useState)(null),'
NEW_STATE = '[_dmReplyTo,_setDmReplyTo]=(0,_.useState)(null),[_dmPickerId,_setDmPickerId]=(0,_.useState)(null),'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _dmPickerId state added to Kr')
else:
    errors.append('FAIL: _dmReplyTo state not found')

# ── 2. Remove the illegal useState call from inside .map() ───────────────────
OLD_HOOK = (
    'const _rxs=_msg.reactions||[];'
    'const [_showPicker,_setShowPicker]=(0,_.useState)(!1);'
)
NEW_HOOK = 'const _rxs=_msg.reactions||[];'
if OLD_HOOK in content:
    content = content.replace(OLD_HOOK, NEW_HOOK, 1)
    print('OK: illegal useState removed from map')
else:
    errors.append('FAIL: illegal useState in map not found')

# ── 3. Replace _showPicker references with _dmPickerId===_msg.id ──────────────
OLD_PICKER_TOGGLE = 'onClick:()=>_setShowPicker(p=>!p),'
NEW_PICKER_TOGGLE = 'onClick:()=>_setDmPickerId(_dmPickerId===_msg.id?null:_msg.id),'
if OLD_PICKER_TOGGLE in content:
    content = content.replace(OLD_PICKER_TOGGLE, NEW_PICKER_TOGGLE, 1)
    print('OK: picker toggle uses _dmPickerId')
else:
    errors.append('FAIL: picker toggle not found')

OLD_PICKER_SHOW = '_showPicker&&'
NEW_PICKER_SHOW = '_dmPickerId===_msg.id&&'
if OLD_PICKER_SHOW in content:
    content = content.replace(OLD_PICKER_SHOW, NEW_PICKER_SHOW, 1)
    print('OK: picker show condition updated')
else:
    errors.append('FAIL: picker show condition not found')

# Also close picker when reply is tapped
OLD_REPLY_BTN = 'onClick:()=>{_setDmReplyTo(_msg);_setShowPicker(!1);}'
NEW_REPLY_BTN = 'onClick:()=>{_setDmReplyTo(_msg);_setDmPickerId(null);}'
if OLD_REPLY_BTN in content:
    content = content.replace(OLD_REPLY_BTN, NEW_REPLY_BTN, 1)
    print('OK: reply button closes picker via _dmPickerId')
else:
    errors.append('FAIL: reply button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
