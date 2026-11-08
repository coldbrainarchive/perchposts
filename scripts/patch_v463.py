#!/usr/bin/env python3
"""Patch v462 -> v463:
Update all 6 sz=13 bird render sites (search filter chip, search dropdown
user results, huddle tags, invite picker) to use the same inline-flex 16x16
badge structure as Xn (postcard/feed pills), so birds look identical everywhere.
Also remove display:block from their emoji spans to match Xn.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v462.js'
dst = '_deploy/assets/index-DUcNPOLc-v463.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Outer span: inline-block 13x13 → inline-flex 16x16 (all 6) ────────────
OLD_OUTER = ('style:{position:`relative`,display:`inline-block`,'
             'fontSize:13,lineHeight:1,width:`13px`,height:`13px`}')
NEW_OUTER = ('style:{position:`relative`,display:`inline-flex`,'
             'alignItems:`center`,justifyContent:`center`,width:16,height:16,'
             'verticalAlign:`middle`,flexShrink:0}')
n = content.count(OLD_OUTER)
if n == 6:
    content = content.replace(OLD_OUTER, NEW_OUTER)
    print(f'OK: sz=13 outer spans updated ({n} occurrences)')
else:
    errors.append(f'FAIL: expected 6 sz=13 outer spans, found {n}')

# ── 2. Emoji span: remove display:block (all 6) ───────────────────────────────
OLD_EMJ = 'style:{filter:_jd.f||``,display:`block`},children:_jd.e||`🐦`'
NEW_EMJ = 'style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`🐦`'
n2 = content.count(OLD_EMJ)
if n2 == 6:
    content = content.replace(OLD_EMJ, NEW_EMJ)
    print(f'OK: display:block removed from _jd emoji spans ({n2} occurrences)')
else:
    errors.append(f'FAIL: expected 6 _jd emoji spans, found {n2}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
