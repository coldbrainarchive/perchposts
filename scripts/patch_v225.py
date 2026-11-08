#!/usr/bin/env python3
"""Patch v224 -> v225: move _lRef to Vr (was wrongly placed in Lr)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v224.js'
dst = '_deploy/assets/index-DUcNPOLc-v225.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove _lRef from Lr (wrong location) ─────────────────────────────────
OLD_WRONG = ',c=(0,_.useRef)(null),_lRef=(0,_.useRef)(0),l=(0,_.useRef)(null)'
NEW_WRONG = ',c=(0,_.useRef)(null),l=(0,_.useRef)(null)'
if OLD_WRONG in content:
    content = content.replace(OLD_WRONG, NEW_WRONG, 1)
    print('OK: _lRef removed from Lr')
else:
    errors.append('FAIL: wrong _lRef location not found')

# ── 2. Add _lRef into Vr — anchor on [o,s]=useState(10) which is Vr-unique ──
OLD_VR_STATE = '[o,s]=(0,_.useState)(10),[SR,setSR]'
NEW_VR_STATE = '[o,s]=(0,_.useState)(10),_lRef=(0,_.useRef)(0),[SR,setSR]'
if OLD_VR_STATE in content:
    content = content.replace(OLD_VR_STATE, NEW_VR_STATE, 1)
    print('OK: _lRef added into Vr')
else:
    errors.append('FAIL: Vr state anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
