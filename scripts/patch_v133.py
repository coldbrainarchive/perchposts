#!/usr/bin/env python3
"""Patch v132 -> v133: SVG chick with coloured body/beak/eyes + random polka dots."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v132.js'
dst = '_deploy/assets/index-DUcNPOLc-v133.js'

# Read and find exact strings
raw = open(src, 'rb').read()
content = raw.decode('utf-8')
errors = []

CHICK = '\U0001f424'  # 🐤

# ── 1. Inject _mkBird ────────────────────────────────────────────────────────
INJECT_AFTER = '}}).catch(function(){{}});var e=Object.create'
BIRD_FN = (
    'function _mkBird(bH,bkH,eH,dots,sz){'
    'var bc=`hsl(${bH},78%,65%)`,bL=`hsl(${bH},78%,73%)`,bD=`hsl(${bH},72%,55%)`,'
    'bk=`hsl(${bkH},85%,55%)`,ey=`hsl(${eH},75%,28%)`,'
    'de=dots.map(function(d,i){'
    'return(0,L.jsx)("circle",{cx:d.x,cy:d.y,r:d.r,fill:`hsl(${d.h},82%,60%)`,opacity:0.72},i)});'
    'return(0,L.jsxs)("svg",{viewBox:"0 0 20 20",width:sz,height:sz,'
    'style:{display:"inline-block",verticalAlign:"middle",overflow:"visible"},'
    'children:['
    '(0,L.jsx)("circle",{cx:10,cy:13,r:7,fill:bc}),'
    '(0,L.jsx)("circle",{cx:10,cy:7.5,r:5,fill:bL}),'
    '(0,L.jsx)("ellipse",{cx:4,cy:13,rx:2.5,ry:3.5,fill:bD}),'
    '(0,L.jsx)("ellipse",{cx:16,cy:13,rx:2.5,ry:3.5,fill:bD}),'
    '(0,L.jsx)("polygon",{points:"13.5,7.5 17,8.5 13.5,9.5",fill:bk}),'
    '(0,L.jsx)("circle",{cx:8.5,cy:6.5,r:2,fill:"white"}),'
    '(0,L.jsx)("circle",{cx:8.8,cy:6.5,r:1.2,fill:ey}),'
    '(0,L.jsx)("circle",{cx:9.2,cy:6.1,r:0.45,fill:"white"}),'
    '(0,L.jsx)("path",{d:"M8.5,19.5 L7.5,21 M10,19.5 L10,21 M11.5,19.5 L12.5,21",'
    'stroke:bk,strokeWidth:0.8,strokeLinecap:"round"}),'
    '...de]})}'
)
if INJECT_AFTER in content:
    content = content.replace(INJECT_AFTER, '}}).catch(function(){{}});' + BIRD_FN + 'var e=Object.create', 1)
    print('OK: _mkBird injected')
else:
    errors.append('FAIL: injection point not found')

# ── 2. Replace Jn regular-user block (find by landmarks) ─────────────────────
START_MARKER = 'var _s=e.username||(e.browser_id||``).slice(0,8);if(!_s)return null;'
END_MARKER   = '}}var Yn={'
idx_start = content.find(START_MARKER)
idx_end   = content.find(END_MARKER, idx_start)
if idx_start >= 0 and idx_end >= 0:
    old_block = content[idx_start:idx_end + 2]  # include the }}
    new_block = (
        'var _s=e.username||(e.browser_id||``).slice(0,8);if(!_s)return null;'
        'var _h=0;for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
        'var _a=Math.abs(_h),_bH=_a%360,_bkH=(_a*7+37)%360,_eH=(_a*13+151)%360,_d=[];'
        'if(_a%2===0){var _nd=(_a%3)+1;'
        'for(var _di=0;_di<_nd;_di++){var _dv=_a>>(_di*5+3);'
        '_d.push({x:(_dv%10)+5,y:((_dv>>4)%8)+10,r:((_dv>>8)%2)+1,h:(_dv>>10)%360})}}'
        'return _mkBird(_bH,_bkH,_eH,_d,"1em")}'
    )
    content = content.replace(old_block, new_block, 1)
    print('OK: Jn returns SVG bird')
else:
    errors.append(f'FAIL: Jn block not found (start={idx_start}, end={idx_end})')

# ── 3. Simplify badge render ──────────────────────────────────────────────────
OLD_BADGE = 'style:typeof i===`object`?{filter:i.f,display:`inline-block`}:{},children:typeof i===`object`?i.e:i'
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, 'children:i', 1)
    print('OK: badge render simplified')
else:
    errors.append('FAIL: badge render not found')

# ── 4. Replace signup bird with 48px _mkBird ─────────────────────────────────
SIGNUP_START = 'position:`absolute`,left:12,fontSize:36,lineHeight:1,'
SIGNUP_END   = f"children:`{CHICK}`}})"
if SIGNUP_START in content:
    idx = content.find(SIGNUP_START)
    chunk = content[idx:]
    end_idx = chunk.find(SIGNUP_END)
    if end_idx >= 0:
        old_seg = chunk[:end_idx + len(SIGNUP_END)]
        new_seg = (
            f'...[_gu?(()=>{{'
            'var _h=0,_s=_gu;'
            'for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
            'var _a=Math.abs(_h),_bH=_a%360,_bkH=(_a*7+37)%360,_eH=(_a*13+151)%360,_d=[];'
            'if(_a%2===0){var _nd=(_a%3)+1;'
            'for(var _di=0;_di<_nd;_di++){var _dv=_a>>(_di*5+3);'
            '_d.push({x:(_dv%10)+5,y:((_dv>>4)%8)+10,r:((_dv>>8)%2)+1.5,h:(_dv>>10)%360})}}'
            f'return _mkBird(_bH,_bkH,_eH,_d,"48px")'
            f'}})()'
            f':(0,L.jsx)(`span`,{{style:{{fontSize:48,lineHeight:1}},children:`{CHICK}`}})]'
        )
        content = content.replace(old_seg, new_seg, 1)
        print('OK: signup bird → 48px SVG _mkBird')
    else:
        errors.append('FAIL: signup bird end marker not found')
else:
    errors.append('FAIL: signup bird start not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
