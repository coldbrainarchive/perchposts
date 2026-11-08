#!/usr/bin/env python3
"""Patch v444 -> v445:
Add spots (_spEls) to all small bird pill renders in search chips, search results,
invite pickers — every place that was rendering the bird emoji without spots.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v444.js'
dst = '_deploy/assets/index-DUcNPOLc-v445.js'

content = open(src, encoding='utf-8').read()
errors = []

SPOTS = ',...(_jd.s?_spEls(_jd.s,13):[])'

# ── Pattern A: search bar chip (filter:_jd.f||``) ────────────────────────────
OLD_A = '(0,L.jsx)(`span`,{style:{filter:_jd.f||``},children:_jd.e||`🐦`})'
NEW_A = '(0,L.jsxs)(`span`,{style:{filter:_jd.f||``,position:`relative`,display:`inline-block`,lineHeight:1},children:[_jd.e||`🐦`' + SPOTS + ']})'
if OLD_A in content:
    content = content.replace(OLD_A, NEW_A)
    print(f'OK: Pattern A fixed ({content.count(NEW_A)} occurrence)')
else:
    errors.append('FAIL: Pattern A not found')

# ── Pattern B: all pill renders (filter:_jd.f?{...}:{}) ──────────────────────
OLD_B = '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`🐦`})'
NEW_B = '(0,L.jsxs)(`span`,{style:{filter:_jd.f||``,position:`relative`,display:`inline-block`,lineHeight:1},children:[_jd.e||`🐦`' + SPOTS + ']})'
count_b = content.count(OLD_B)
if count_b > 0:
    content = content.replace(OLD_B, NEW_B)
    print(f'OK: Pattern B fixed ({count_b} occurrences)')
else:
    errors.append('FAIL: Pattern B not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
