#!/usr/bin/env python3
"""Patch v526 -> v527: Clan name not all-caps, smaller font for values to fit mobile."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v526.js'
dst = '_deploy/assets/index-DUcNPOLc-v527.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── User card ─────────────────────────────────────────────────────────────────

# Remove toUpperCase from clan value + shrink font
OLD_CV = 'fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_clan.n.toUpperCase()}'
NEW_CV = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_clan.n}'
if OLD_CV in content:
    content = content.replace(OLD_CV, NEW_CV, 1)
    print('OK: user card clan value: no caps, smaller font')
else:
    errors.append('FAIL: user card clan value not found')

# Shrink date value font to match
OLD_DV = 'fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),_clan&&'
NEW_DV = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),_clan&&'
if OLD_DV in content:
    content = content.replace(OLD_DV, NEW_DV, 1)
    print('OK: user card date value font shrunk')
else:
    errors.append('FAIL: user card date value not found')

# ── Nest panel ────────────────────────────────────────────────────────────────

# Remove toUpperCase from clan value + shrink font
OLD_CNV = 'fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_clanN.n.toUpperCase()}'
NEW_CNV = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_clanN.n}'
if OLD_CNV in content:
    content = content.replace(OLD_CNV, NEW_CNV, 1)
    print('OK: Nest clan value: no caps, smaller font')
else:
    errors.append('FAIL: Nest clan value not found')

# Shrink date value font to match
OLD_DNV = 'fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd||`—`})]}),_clanN'
NEW_DNV = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_hd||`—`})]}),_clanN'
if OLD_DNV in content:
    content = content.replace(OLD_DNV, NEW_DNV, 1)
    print('OK: Nest date value font shrunk')
else:
    errors.append('FAIL: Nest date value not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
