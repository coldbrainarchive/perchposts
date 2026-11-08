#!/usr/bin/env python3
"""Patch v134 -> v135: use 🐤🐦🐧 as base emojis with hue-rotate + spot filters."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v134.js'
dst = '_deploy/assets/index-DUcNPOLc-v135.js'

content = open(src, encoding='utf-8').read()
errors = []

BIRDS = '[\`\U0001f424\`,\`\U0001f426\`,\`\U0001f427\`]'

# Shared hash + filter logic (returns {e, f})
def bird_logic(src_var):
    return (
        f'var _h=0,_s={src_var};'
        'for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
        f'var _a=Math.abs(_h),_e={BIRDS}[_a%3],'
        '_f=`hue-rotate(${_a%360}deg)`;'
        'if(_a%3!==0){'
        'var _h1=(_a*7+137)%360,_h2=(_a*13+251)%360,'
        '_ox1=((_a>>4)%5)+2,_oy1=-((_a>>7)%5)-2,'
        '_ox2=-((_a>>10)%4)-1,_oy2=((_a>>13)%4)+2;'
        'if(_a%3===1)_f+=` drop-shadow(${_ox1}px ${_oy1}px 0px hsl(${_h1},90%,58%))`;'
        'else _f+=` drop-shadow(${_ox1}px ${_oy1}px 0px hsl(${_h1},90%,58%))'
        ' drop-shadow(${_ox2}px ${_oy2}px 0px hsl(${_h2},90%,58%))`;'
        '}'
    )

# ── 1. Jn regular-user block ─────────────────────────────────────────────────
OLD_JN = (
    'var _s=e.username||(e.browser_id||``).slice(0,8);if(!_s)return null;'
    'var _h=0;for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
    'var _a=Math.abs(_h),_bH=_a%360,_bkH=(_a*7+37)%360,_eH=(_a*13+151)%360,_d=[];'
    'if(_a%2===0){var _nd=(_a%3)+1;'
    'for(var _di=0;_di<_nd;_di++){var _dv=_a>>(_di*5+3);'
    '_d.push({x:(_dv%10)+5,y:((_dv>>4)%8)+10,r:((_dv>>8)%2)+1,h:(_dv>>10)%360})}}'
    'return _mkBird(_bH,_bkH,_eH,_d,"1em")}'
)
NEW_JN = (
    'var _s=e.username||(e.browser_id||``).slice(0,8);if(!_s)return null;'
    + bird_logic('_s') +
    'return{e:_e,f:_f}}'
)
if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: Jn picks from 🐤🐦🐧 with hue-rotate filter')
else:
    errors.append('FAIL: Jn segment not found')

# ── 2. Badge render: restore filter+children approach ────────────────────────
OLD_BADGE = 'className:`user-pill-badge`,children:i'
NEW_BADGE = (
    'className:`user-pill-badge`,'
    'style:typeof i===`object`&&i.f?{filter:i.f,display:`inline-block`}:{},'
    'children:typeof i===`object`&&i.e?i.e:i'
)
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: badge render restored with filter')
else:
    errors.append('FAIL: badge render not found')

# ── 3. Signup bird: emoji + filter at 40px ───────────────────────────────────
OLD_SIGNUP = (
    'children:[_gu?(()=>{var _h=0,_s=_gu;'
    'for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
    'var _a=Math.abs(_h),_bH=_a%360,_bkH=(_a*7+37)%360,_eH=(_a*13+151)%360,_d=[];'
    'if(_a%2===0){var _nd=(_a%3)+1;'
    'for(var _di=0;_di<_nd;_di++){var _dv=_a>>(_di*5+3);'
    '_d.push({x:(_dv%10)+5,y:((_dv>>4)%8)+10,r:((_dv>>8)%2)+1.5,h:(_dv>>10)%360})}}'
    'return _mkBird(_bH,_bkH,_eH,_d,"48px")})():'
    '(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:48,lineHeight:1},children:`\U0001f424`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:14,fontWeight:700,'
    'color:_gu?`#0a0a0a`:`#64748b`,letterSpacing:`-0.01em`,textAlign:`center`},'
    'children:_gu||`tap to generate username`})]'
)
NEW_SIGNUP = (
    'children:[_gu?(()=>{'
    + bird_logic('_gu') +
    'return(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:40,lineHeight:1,filter:_f},children:_e})'
    '})():(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:40,lineHeight:1},children:`\U0001f424`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:14,fontWeight:700,'
    'color:_gu?`#0a0a0a`:`#64748b`,letterSpacing:`-0.01em`,textAlign:`center`},'
    'children:_gu||`tap to generate username`})]'
)
if OLD_SIGNUP in content:
    content = content.replace(OLD_SIGNUP, NEW_SIGNUP, 1)
    print('OK: signup bird shows correct emoji+filter at 40px')
else:
    errors.append('FAIL: signup bird segment not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
