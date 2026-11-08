#!/usr/bin/env python3
"""Patch v458 -> v459:
Fix polkadot spots being misaligned on Chrome vs Safari.

Root cause: _spEls positions spots in absolute pixels based on sz, but Chrome
and Safari render emoji glyphs at slightly different offsets within the em box.
Fix: switch spots to percentage positioning so they're relative to the
container box, and give each outer bird span explicit width+height so the
container is always exactly sz x sz pixels regardless of browser.

sz=40 outer span already had explicit dimensions — no change needed there.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v458.js'
dst = '_deploy/assets/index-DUcNPOLc-v459.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Switch _spEls to percentage positioning ────────────────────────────────
OLD_SP = ("width:sz*s.w+'px',height:sz*(s.wh||s.w)+'px',"
          "left:sz*s.x+'px',top:sz*s.y+'px'")
NEW_SP = ("width:s.w*100+'%',height:(s.wh||s.w)*100+'%',"
          "left:s.x*100+'%',top:s.y*100+'%'")
if OLD_SP in content:
    content = content.replace(OLD_SP, NEW_SP, 1)
    print('OK: _spEls switched to % positioning')
else:
    errors.append('FAIL: _spEls pixel positioning not found')

# ── 2. sz=13 outer spans — add fontSize + explicit box (6 occurrences) ────────
OLD_13 = 'style:{position:`relative`,display:`inline-block`,lineHeight:1},children:[(0,L.jsx)(`span`'
NEW_13 = 'style:{position:`relative`,display:`inline-block`,fontSize:13,lineHeight:1,width:`13px`,height:`13px`},children:[(0,L.jsx)(`span`'
c13 = content.count(OLD_13)
if c13 > 0:
    content = content.replace(OLD_13, NEW_13)
    print(f'OK: sz=13 outer spans fixed ({c13} occurrences)')
else:
    errors.append('FAIL: sz=13 outer span not found')

# ── 3. sz=17 outer span — add explicit box ────────────────────────────────────
OLD_17 = 'style:{position:`relative`,display:`inline-block`,fontSize:17,lineHeight:1,flexShrink:0}'
NEW_17 = 'style:{position:`relative`,display:`inline-block`,fontSize:17,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`}'
if OLD_17 in content:
    content = content.replace(OLD_17, NEW_17, 1)
    print('OK: sz=17 outer span fixed')
else:
    errors.append('FAIL: sz=17 outer span not found')

# ── 4. sz=32 outer span — add explicit box ────────────────────────────────────
OLD_32 = 'style:{position:`relative`,display:`inline-block`,fontSize:32,lineHeight:1}'
NEW_32 = 'style:{position:`relative`,display:`inline-block`,fontSize:32,lineHeight:1,width:`32px`,height:`32px`}'
if OLD_32 in content:
    content = content.replace(OLD_32, NEW_32, 1)
    print('OK: sz=32 outer span fixed')
else:
    errors.append('FAIL: sz=32 outer span not found')

# ── 5. sz=56 outer span — add explicit box ────────────────────────────────────
OLD_56 = 'style:{position:`relative`,display:`inline-block`,fontSize:56,lineHeight:1}'
NEW_56 = 'style:{position:`relative`,display:`inline-block`,fontSize:56,lineHeight:1,width:`56px`,height:`56px`}'
if OLD_56 in content:
    content = content.replace(OLD_56, NEW_56, 1)
    print('OK: sz=56 outer span fixed')
else:
    errors.append('FAIL: sz=56 outer span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
