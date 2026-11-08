#!/usr/bin/env python3
"""Patch v292 -> v293: make time and bot filter chips look like pill tags
with solid accent colour (#c084fc) and dark text (#0a0a0a), like the Random board."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v292.js'
dst = '_deploy/assets/index-DUcNPOLc-v293.js'

content = open(src, encoding='utf-8').read()
errors = []

PILL = (
    'display:`inline-flex`,alignItems:`center`,gap:5,'
    'height:22,padding:`0 8px`,borderRadius:999,'
    'border:`1px solid rgba(0,0,0,0.15)`,'
    'background:`#c084fc`,color:`#0a0a0a`,'
    'fontSize:10,fontWeight:800,letterSpacing:`0.03em`,'
    'textTransform:`uppercase`,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,'
    'cursor:`pointer`'
)

# ── 1. Time chip in search bar (q2 active) ───────────────────────────────────
OLD_TIME_CHIP = (
    'q2&&(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
    'style:{background:`rgba(192,132,252,0.15)`,borderColor:`#c084fc55`,color:`#c084fc`},'
    'onClick:e=>{e.stopPropagation(),ae()},children:[(0,L.jsx)(`span`,{children:`🕐 `'
    '+(q2&&q2.startsWith(`ago_`)?q2.slice(4)+`h ago`:q2)})]}'
)
NEW_TIME_CHIP = (
    'q2&&(0,L.jsxs)(`button`,{type:`button`,'
    f'style:{{{PILL}}},'
    'onClick:e=>{e.stopPropagation(),ae()},children:[(0,L.jsx)(`span`,{children:`🕐 `'
    '+(q2&&q2.startsWith(`ago_`)?q2.slice(4)+`h ago`:q2)})]}'
)
if OLD_TIME_CHIP in content:
    content = content.replace(OLD_TIME_CHIP, NEW_TIME_CHIP, 1)
    print('OK: time chip styled as pill')
else:
    errors.append('FAIL: time chip not found')

# ── 2. Bot chip in search bar ─────────────────────────────────────────────────
OLD_BOT_CHIP = (
    '_botF&&(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
    'style:{background:`rgba(192,132,252,0.15)`,borderColor:`#c084fc55`,color:`#c084fc`},'
    'onClick:e=>{e.stopPropagation(),_clearBot()},children:[(0,L.jsx)(`span`,{children:`🤖 Bots`})]}'
)
NEW_BOT_CHIP = (
    '_botF&&(0,L.jsxs)(`button`,{type:`button`,'
    f'style:{{{PILL}}},'
    'onClick:e=>{e.stopPropagation(),_clearBot()},children:[(0,L.jsx)(`span`,{children:`🤖 Bots`})]}'
)
if OLD_BOT_CHIP in content:
    content = content.replace(OLD_BOT_CHIP, NEW_BOT_CHIP, 1)
    print('OK: bot chip styled as pill')
else:
    errors.append('FAIL: bot chip not found')

# ── 3. Clock toggle button in dropdown (🕐 icon, opens time panel) ────────────
OLD_CLOCK_BTN = (
    'onClick:()=>W(!P),style:{position:`absolute`,top:8,right:8,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,'
    'width:22,height:22,borderRadius:999,border:`none`,'
    'background:P?`rgba(192,132,252,0.2)`:`#2d2f3a`,'
    'color:P||q2?`#c084fc`:`#94a3b8`,fontSize:13,lineHeight:1,cursor:`pointer`,padding:0}'
)
NEW_CLOCK_BTN = (
    'onClick:()=>W(!P),style:{position:`absolute`,top:8,right:8,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,'
    'width:28,height:22,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
    'background:P||q2?`#c084fc`:`#2d2f3a`,'
    'color:P||q2?`#0a0a0a`:`#94a3b8`,fontSize:13,lineHeight:1,cursor:`pointer`,padding:0}'
)
if OLD_CLOCK_BTN in content:
    content = content.replace(OLD_CLOCK_BTN, NEW_CLOCK_BTN, 1)
    print('OK: clock toggle button styled as pill')
else:
    errors.append('FAIL: clock button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
