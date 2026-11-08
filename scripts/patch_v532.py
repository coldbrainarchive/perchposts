#!/usr/bin/env python3
"""Patch v531 -> v532: Explicitly set textAlign:center on every child div in all Nest columns."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v531.js'
dst = '_deploy/assets/index-DUcNPOLc-v532.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Nest label divs: add textAlign:center explicitly ─────────────────────────
OLD_LBL = 'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`}'
NEW_LBL = 'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`,textAlign:`center`,width:`100%`}'
count = content.count(OLD_LBL)
if count > 0:
    content = content.replace(OLD_LBL, NEW_LBL)
    print(f'OK: textAlign:center + width:100% added to {count} Nest label divs')
else:
    errors.append('FAIL: Nest label div style not found')

# ── Nest value divs: add textAlign:center explicitly ─────────────────────────
OLD_VAL_HD = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_hd||`—`'
NEW_VAL_HD = 'fontSize:13,color:`#f1f5f9`,fontWeight:700,textAlign:`center`,width:`100%`},children:_hd||`—`'
if OLD_VAL_HD in content:
    content = content.replace(OLD_VAL_HD, NEW_VAL_HD, 1)
    print('OK: textAlign:center added to Nest date value')
else:
    errors.append('FAIL: Nest date value not found')

OLD_VAL_WC = 'fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc'
NEW_VAL_WC = 'fontSize:22,color:`#f1f5f9`,fontWeight:700,textAlign:`center`,width:`100%`},children:_wc'
if OLD_VAL_WC in content:
    content = content.replace(OLD_VAL_WC, NEW_VAL_WC, 1)
    print('OK: textAlign:center added to Nest worm value')
else:
    # try 13px version
    OLD_VAL_WC2 = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_wc'
    NEW_VAL_WC2 = 'fontSize:13,color:`#f1f5f9`,fontWeight:700,textAlign:`center`,width:`100%`},children:_wc'
    if OLD_VAL_WC2 in content:
        content = content.replace(OLD_VAL_WC2, NEW_VAL_WC2, 1)
        print('OK: textAlign:center added to Nest worm value (13px)')
    else:
        errors.append('FAIL: Nest worm value not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
