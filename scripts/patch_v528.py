#!/usr/bin/env python3
"""Patch v527 -> v528:
- Add textAlign:center to all columns so Hatched content is truly centred
- Match worm count font size (18/22) to 13px to match date and clan
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v527.js'
dst = '_deploy/assets/index-DUcNPOLc-v528.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add textAlign:center to COL (user card columns) ───────────────────────
OLD_COL = 'flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`10px 8px`'
NEW_COL = 'flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`'
count = content.count(OLD_COL)
if count > 0:
    content = content.replace(OLD_COL, NEW_COL)
    print(f'OK: textAlign:center added to user card columns ({count} occurrences)')
else:
    errors.append('FAIL: user card COL style not found')

# ── 2. Add textAlign:center to COLN (Nest columns) ───────────────────────────
OLD_COLN = 'flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`12px 8px`'
NEW_COLN = 'flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`'
count = content.count(OLD_COLN)
if count > 0:
    content = content.replace(OLD_COLN, NEW_COLN)
    print(f'OK: textAlign:center added to Nest columns ({count} occurrences)')
else:
    errors.append('FAIL: Nest COLN style not found')

# ── 3. Match worm count font size in user card (18 -> 13) ────────────────────
OLD_WC = 'fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc'
NEW_WC = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_wc'
if OLD_WC in content:
    content = content.replace(OLD_WC, NEW_WC, 1)
    print('OK: user card worm count font 18->13')
else:
    errors.append('FAIL: user card worm count font not found')

# ── 4. Match worm count font size in Nest (22 -> 13) ─────────────────────────
OLD_WCN = 'fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc'
NEW_WCN = 'fontSize:13,color:`#f1f5f9`,fontWeight:700},children:_wc'
if OLD_WCN in content:
    content = content.replace(OLD_WCN, NEW_WCN, 1)
    print('OK: Nest worm count font 22->13')
else:
    errors.append('FAIL: Nest worm count font not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
