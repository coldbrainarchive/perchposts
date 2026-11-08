#!/usr/bin/env python3
"""Patch v441 -> v442:
- Hide "Add Birds" placeholder once a user is selected
- Slimmer invite button (keep username in text)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v441.js'
dst = '_deploy/assets/index-DUcNPOLc-v442.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Hide placeholder when a user is already selected ──────────────────────
OLD_PH = 'placeholder:`Add Birds`'
NEW_PH = 'placeholder:_wpInvP?``:``Add Birds``'
# simpler: just use empty string when pending
NEW_PH = "placeholder:_wpInvP?``:` Add Birds`"
if OLD_PH in content:
    # Only replace the one inside the inline invite picker (not new post form)
    idx = content.find('c?.is_huddle&&_wpInvOpen&&(0,L.jsxs)')
    ph_idx = content.find(OLD_PH, idx)
    if ph_idx != -1:
        content = content[:ph_idx] + "placeholder:_wpInvP?``:` Add Birds`" + content[ph_idx+len(OLD_PH):]
        print('OK: placeholder hidden when user selected')
    else:
        errors.append('FAIL: placeholder not found in invite picker')
else:
    errors.append('FAIL: Add Birds placeholder not found')

# ── 2. Slimmer invite button ──────────────────────────────────────────────────
OLD_BTN = 'width:`100%`,marginTop:8,padding:`8px`,borderRadius:8,border:`none`,background:`#c084fc`,color:`#fff`,fontWeight:700,fontSize:13,cursor:`pointer`'
NEW_BTN = 'width:`100%`,marginTop:6,padding:`6px 10px`,borderRadius:8,border:`none`,background:`#c084fc`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`'
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: invite button slimmer')
else:
    errors.append('FAIL: invite button style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
