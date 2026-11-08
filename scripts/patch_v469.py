#!/usr/bin/env python3
"""Patch v468 -> v469:
1. Add -webkit-text-size-adjust:100% to .user-pill CSS — prevents iOS from
   auto-scaling the CSS class font-size (inline styles are unaffected by
   iOS text-size-adjust, causing Xn pills to appear larger than search chips).
2. Replace the search active user filter chip's manual pill span with Xn —
   makes both contexts share literally identical code, eliminating any
   remaining rendering difference on any platform.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v468.js'
dst = '_deploy/assets/index-DUcNPOLc-v469.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add text-size-adjust to .user-pill CSS ─────────────────────────────────
OLD_CSS = ('        box-sizing: border-bo')
# Find the closing of user-pill block
idx = content.find('.user-pill {')
block_end = content.find('\n      }', idx)
old_block_end = content[block_end:block_end+10]
new_insert = '\n        -webkit-text-size-adjust: 100%;\n        text-size-adjust: 100%;'
if 'text-size-adjust' not in content[idx:block_end]:
    content = content[:block_end] + new_insert + content[block_end:]
    print('OK: text-size-adjust added to .user-pill')
else:
    print('NOTE: text-size-adjust already present')

# ── 2. Replace manual search chip pill with Xn ────────────────────────────────
OLD_CHIP = ('children:(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
            'gap:4,height:22,padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
            'background:(_adminUsers.has(m.toLowerCase())||(()=>{const _ua=UR.find(_f=>'
            '_f.username.toLowerCase()===m.toLowerCase());if(_ua?.role===`admin`)_addAdmin(m);'
            'return _ua?.role===`admin`;})()?!0:!1)?`#ffffff`:Hn(null,m),color:`#0a0a0a`,'
            'fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,'
            'boxSizing:`border-box`},children:[_adminUsers.has(m.toLowerCase())?(0,L.jsx)(`img`,'
            '{src:`/admin-bird.png`,style:{height:16,width:16,objectFit:`contain`,display:`block`,'
            'flexShrink:0}}):(()=>{const _jd=Jn({username:m,browser_id:null})||{};return'
            '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`,'
            'justifyContent:`center`,fontSize:_bsz,width:16,height:16,verticalAlign:`middle`,'
            'flexShrink:0},children:[(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},'
            'children:_jd.e||`🐦`}),...(_jd.s?_spEls(_jd.s,13):[])]});})(),'
            '(0,L.jsx)(`span`,{children:m})]})}'  )
NEW_CHIP = ('children:(0,L.jsx)(Xn,{record:{username:m,browser_id:null,'
            'is_admin:_adminUsers.has(m.toLowerCase())},name:m,color:Hn(null,m)})}')
if OLD_CHIP in content:
    content = content.replace(OLD_CHIP, NEW_CHIP, 1)
    print('OK: search filter chip replaced with Xn')
else:
    errors.append('FAIL: search chip pill not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
