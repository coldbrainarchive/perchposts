#!/usr/bin/env python3
"""Patch v396 -> v397:
- Clear all hidden by default
- Tap Notifications tab again (while on it) to reveal/toggle Clear all
- Navigating away hides it; panel close resets state automatically
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v396.js'
dst = '_deploy/assets/index-DUcNPOLc-v397.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _showClear state ───────────────────────────────────────────────────
OLD_STATE = '[g,v]=(0,_.useState)(!0)'
NEW_STATE = '[g,v]=(0,_.useState)(!0),[_showClear,_setShowClear]=(0,_.useState)(!1)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _showClear state added')
else:
    errors.append('FAIL: panel state not found')

# ── 2. Tab click: double-tap notifications to toggle, hide on other tabs ──────
OLD_TAB = 'onClick:()=>l(e.id)'
NEW_TAB = (
    'onClick:()=>{'
    'if(e.id===c&&e.id===`notifications`){_setShowClear(v=>!v);}'
    'else{if(e.id!==`notifications`)_setShowClear(!1);l(e.id);}}'
)
if OLD_TAB in content:
    content = content.replace(OLD_TAB, NEW_TAB, 1)
    print('OK: tab click toggles _showClear')
else:
    errors.append('FAIL: tab onClick not found')

# ── 3. Guard Clear all behind _showClear ──────────────────────────────────────
OLD_BTN = 'j.length>0&&(0,L.jsx)(`button`,{type:`button`,'
NEW_BTN = '_showClear&&j.length>0&&(0,L.jsx)(`button`,{type:`button`,'
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: Clear all guarded by _showClear')
else:
    errors.append('FAIL: Clear all button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
