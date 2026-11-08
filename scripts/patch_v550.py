#!/usr/bin/env python3
"""Patch v549 -> v550:
- Add data-gpb attribute to Xn user pills (username as value)
- Global _gpBird state in qr() App component
- Document capture click handler intercepts [data-gpb] clicks, stops propagation,
  opens overlay instead of navigating
- Global overlay (same style as comment Bird overlay) rendered at app root
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v549.js'
dst = '_deploy/assets/index-DUcNPOLc-v550.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add data-gpb attr + cursor fix to Xn span ─────────────────────────────
OLD_XN = ('className:`user-pill`,style:{color:N?`#ffffff`:`#0a0a0a`,'
          'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
          'borderColor:o?`rgba(0,0,0,0.15)`:s?`#c084fc`:N?`#ef4444`:c,'
          'cursor:r?`pointer`:`default`},onClick:r,')
NEW_XN = ('className:`user-pill`,style:{color:N?`#ffffff`:`#0a0a0a`,'
          'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
          'borderColor:o?`rgba(0,0,0,0.15)`:s?`#c084fc`:N?`#ef4444`:c,'
          'cursor:t?`pointer`:`default`},'
          '`data-gpb`:t||null,onClick:r,')
if OLD_XN in content:
    content = content.replace(OLD_XN, NEW_XN, 1)
    print('OK: data-gpb added to Xn span')
else:
    errors.append('FAIL: Xn span props not found')

# ── 2. Add _gpBird state to qr() ─────────────────────────────────────────────
OLD_STATE = '[_dmInit,_setDmInit]=(0,_.useState)(null),[f,p]=(0,_.useState)(0)'
NEW_STATE = '[_dmInit,_setDmInit]=(0,_.useState)(null),[_gpBird,_setGpBird]=(0,_.useState)(null),[f,p]=(0,_.useState)(0)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _gpBird state added to qr()')
else:
    errors.append('FAIL: _dmInit state not found in qr()')

# ── 3. Add document capture click handler to existing event listener effect ───
OLD_EFF = ('let _odm=ev=>{_setDmInit(ev.detail);d(!0)};'
           'return window.addEventListener(`like-no-auth`,e),'
           'window.addEventListener(`open-dm`,_odm),'
           '()=>{window.removeEventListener(`like-no-auth`,e);'
           'window.removeEventListener(`open-dm`,_odm)}')
NEW_EFF = ('let _odm=ev=>{_setDmInit(ev.detail);d(!0)};'
           'const _hgpb=ev=>{'
           'const el=ev.target.closest(`[data-gpb]`);'
           'if(!el)return;'
           'const un=el.getAttribute(`data-gpb`);'
           'if(!un||un.includes(`#`))return;'
           'ev.stopPropagation();'
           '_setGpBird(un);'
           '};'
           'document.addEventListener(`click`,_hgpb,!0);'
           'return window.addEventListener(`like-no-auth`,e),'
           'window.addEventListener(`open-dm`,_odm),'
           '()=>{window.removeEventListener(`like-no-auth`,e);'
           'window.removeEventListener(`open-dm`,_odm);'
           'document.removeEventListener(`click`,_hgpb,!0)}')
if OLD_EFF in content:
    content = content.replace(OLD_EFF, NEW_EFF, 1)
    print('OK: document capture click handler added')
else:
    errors.append('FAIL: event listener effect not found')

# ── 4. Add global overlay JSX to qr() return ─────────────────────────────────
OVERLAY = (
    '_gpBird?'
    '(0,L.jsxs)(`div`,{onClick:()=>_setGpBird(null),'
    'style:{position:`fixed`,inset:0,background:`rgba(0,0,0,0.6)`,zIndex:2000,'
    'display:`flex`,alignItems:`flex-end`,justifyContent:`center`},'
    'children:['
    '(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:`18px 18px 0 0`,'
    'width:`100%`,maxWidth:`480px`,paddingBottom:32,'
    'boxShadow:`0 -8px 40px rgba(0,0,0,0.4)`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{padding:`10px 16px 4px`,display:`flex`,'
    'justifyContent:`center`},'
    'children:(0,L.jsx)(`button`,{onClick:()=>_setGpBird(null),'
    'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,'
    'fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`})}),'
    '(0,L.jsx)(_UserCard,{username:_gpBird}),'
    '(0,L.jsxs)(`div`,{style:{padding:`0 16px`,marginTop:8,'
    'display:`flex`,flexDirection:`column`,gap:8},'
    'children:['
    '_gpBird!==(n===`mod`||n===`admin`?i:o)?'
    '(0,L.jsx)(`a`,{href:`/new?huddle=1&invite=${encodeURIComponent(_gpBird)}`,'
    'style:{display:`block`,textAlign:`center`,padding:`13px`,borderRadius:12,'
    'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,'
    'textDecoration:`none`},children:`Huddle`}):null,'
    '(0,L.jsx)(`a`,{href:`/?user=${encodeURIComponent(_gpBird)}`,'
    'onClick:()=>_setGpBird(null),'
    'style:{display:`block`,textAlign:`center`,padding:`13px`,borderRadius:12,'
    'background:`#1e293b`,color:`#c084fc`,fontWeight:700,fontSize:15,'
    'textDecoration:`none`,border:`1.5px solid #c084fc`},'
    'children:`See Posts`})'
    ']})'
    ']})'
    ']})'
    ':null'
)

OLD_END = ('window.location.href=`/`}})]})})')
NEW_END = ('window.location.href=`/`}}),' + OVERLAY + ']})})')
if OLD_END in content:
    content = content.replace(OLD_END, NEW_END, 1)
    print('OK: global overlay added to qr() return')
else:
    errors.append('FAIL: qr() return closing not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
