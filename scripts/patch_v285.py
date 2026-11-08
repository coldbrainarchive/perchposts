#!/usr/bin/env python3
"""Patch v284 -> v285:
1. Remove textTransform:uppercase from user pills (occurrences 5 & 6) — lowercase names
2. Add useEffect in Lr to fetch user role when m is set from URL nav but UR is empty
   (fixes admin pill showing wrong when clicking username in a post → ?user=borbie)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v284.js'
dst = '_deploy/assets/index-DUcNPOLc-v285.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove uppercase from search-bar user chip (occurrence 5 at ~295907) ──
OLD_CHIP_UPPER = (
    '.role===`admin`?`#ffffff`:Hn(null,m),color:`#0a0a0a`,fontSize:10,fontWeight:800,'
    'letterSpacing:`0.03em`,textTransform:`uppercase`,whiteSpace:`nowrap`,lineHeight:1,'
    'flexShrink:0,boxSizing:`border-box`'
)
NEW_CHIP_LOWER = (
    '.role===`admin`?`#ffffff`:Hn(null,m),color:`#0a0a0a`,fontSize:11,fontWeight:700,'
    'whiteSpace:`nowrap`,lineHeight:1,'
    'flexShrink:0,boxSizing:`border-box`'
)
if OLD_CHIP_UPPER in content:
    content = content.replace(OLD_CHIP_UPPER, NEW_CHIP_LOWER, 1)
    print('OK: search bar user chip lowercase')
else:
    errors.append('FAIL: search bar chip uppercase style not found')

# ── 2. Remove uppercase from dropdown user suggestion pill (occurrence 6) ─────
OLD_SUGG_UPPER = (
    '`admin`?`#ffffff`:Hn(null,_u.username),color:`#0a0a0a`,fontSize:10,fontWeight:800,'
    'letterSpacing:`0.03em`,textTransform:`uppercase`,whiteSpace:`nowrap`,lineHeight:1,'
    'flexShrink:0,boxSizing:`border-box`'
)
NEW_SUGG_LOWER = (
    '`admin`?`#ffffff`:Hn(null,_u.username),color:`#0a0a0a`,fontSize:11,fontWeight:700,'
    'whiteSpace:`nowrap`,lineHeight:1,'
    'flexShrink:0,boxSizing:`border-box`'
)
if OLD_SUGG_UPPER in content:
    content = content.replace(OLD_SUGG_UPPER, NEW_SUGG_LOWER, 1)
    print('OK: dropdown user suggestion lowercase')
else:
    errors.append('FAIL: dropdown suggestion uppercase style not found')

# ── 3. Add role-lookup useEffect after the debounce effect in Lr ───────────────
# When m (user filter) is set from URL nav, UR may be empty, so admin can't be detected.
# Fetch the user's role to populate UR when m is set and UR doesn't contain m.
OLD_AFTER_DEBOUNCE = '},[n]),(0,_.useEffect)(()=>{function e(e){!P&&l.current'
NEW_AFTER_DEBOUNCE = (
    '},[n])'
    # New useEffect: fetch role when m is set but not in UR
    ',(0,_.useEffect)(()=>{'
    'if(!m)return;'
    'if(UR.find(_f=>_f.username===m))return;'
    'fetch(`${R}/search-users?q=${encodeURIComponent(m)}`)'
    '.then(_r=>_r.ok?_r.json():{users:[]})'
    '.then(_d=>{if(_d.users&&_d.users.length)setUR(_d.users);})'
    '.catch(()=>{});'
    '},[m])'
    ',(0,_.useEffect)(()=>{function e(e){!P&&l.current'
)
if OLD_AFTER_DEBOUNCE in content:
    content = content.replace(OLD_AFTER_DEBOUNCE, NEW_AFTER_DEBOUNCE, 1)
    print('OK: role-lookup useEffect added for URL-nav user filter')
else:
    errors.append('FAIL: debounce effect end not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
