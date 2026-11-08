#!/usr/bin/env python3
"""Patch v562 -> v563:
- Restyle attach button: translucent pill circle, vertically centered, matches send button vibe
- Update chat-input-row to center-align items so button sits level with bubble
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v562.js'
dst = '_deploy/assets/index-DUcNPOLc-v563.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# ── 1. chat-input-row: flex-end → center so button aligns with bubble ──
patch(
    '.chat-input-row {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n      }',
    '.chat-input-row {\n        display: flex;\n        align-items: center;\n        gap: 8px;\n      }',
    'chat-input-row align-items: center'
)

# ── 2. Restyle attach button to translucent pill ──
patch(
    'style:{flexShrink:0,background:`none`,border:`none`,color:_cA?`#c084fc`:`#8fa0b6`,fontSize:18,cursor:`pointer`,padding:`0 4px`,lineHeight:1,display:`flex`,alignItems:`center`},title:`Attach photo or video`,children:_cUL?(0,L.jsx)(`span`,{style:{fontSize:12},children:`…`}):`📎`',
    'style:{flexShrink:0,width:32,height:32,borderRadius:999,border:`1px solid rgba(255,255,255,0.08)`,background:_cA?`rgba(192,132,252,0.15)`:`rgba(255,255,255,0.05)`,color:_cA?`#c084fc`:`rgba(255,255,255,0.35)`,fontSize:15,cursor:_cUL||m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,transition:`background 0.15s,color 0.15s`},title:`Attach photo or video`,children:_cUL?(0,L.jsx)(`span`,{style:{fontSize:11},children:`…`}):`📎`',
    'restyle attach button to translucent pill'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
