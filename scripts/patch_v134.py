#!/usr/bin/env python3
"""Patch v133 -> v134: fix broken signup bird — move SVG out of style object."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v133.js'
dst = '_deploy/assets/index-DUcNPOLc-v134.js'

content = open(src, encoding='utf-8').read()
errors = []

BIRD_IIFE = (
    '(()=>{var _h=0,_s=_gu;'
    'for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
    'var _a=Math.abs(_h),_bH=_a%360,_bkH=(_a*7+37)%360,_eH=(_a*13+151)%360,_d=[];'
    'if(_a%2===0){var _nd=(_a%3)+1;'
    'for(var _di=0;_di<_nd;_di++){var _dv=_a>>(_di*5+3);'
    '_d.push({x:(_dv%10)+5,y:((_dv>>4)%8)+10,r:((_dv>>8)%2)+1.5,h:(_dv>>10)%360})}}'
    'return _mkBird(_bH,_bkH,_eH,_d,"48px")})()'
)

NAME_SPAN = (
    '(0,L.jsx)(`span`,{style:{fontSize:14,fontWeight:700,'
    'color:_gu?`#0a0a0a`:`#64748b`,letterSpacing:`-0.01em`,textAlign:`center`},'
    'children:_gu||`tap to generate username`})'
)

FALLBACK_BIRD = (
    '(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:48,lineHeight:1},'
    'children:`\U0001f424`})'
)

OLD = (
    f'children:[(0,L.jsx)(`span`,{{style:{{...[_gu?{BIRD_IIFE}:{FALLBACK_BIRD}],'
    f'{NAME_SPAN}]]'
)

NEW = (
    f'children:[_gu?{BIRD_IIFE}:{FALLBACK_BIRD},'
    f'{NAME_SPAN}]'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: signup bird fixed — SVG now correct sibling in children array')
else:
    # Try building from the exact raw text we found
    OLD_RAW = (
        'children:[(0,L.jsx)(`span`,{style:{...[_gu?(()=>{var _h=0,_s=_gu;'
        'for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
        'var _a=Math.abs(_h),_bH=_a%360,_bkH=(_a*7+37)%360,_eH=(_a*13+151)%360,_d=[];'
        'if(_a%2===0){var _nd=(_a%3)+1;'
        'for(var _di=0;_di<_nd;_di++){var _dv=_a>>(_di*5+3);'
        '_d.push({x:(_dv%10)+5,y:((_dv>>4)%8)+10,r:((_dv>>8)%2)+1.5,h:(_dv>>10)%360})}}'
        'return _mkBird(_bH,_bkH,_eH,_d,"48px")})():'
        '(0,L.jsx)(`span`,{style:{fontSize:48,lineHeight:1},children:`\U0001f424`})],'
        '(0,L.jsx)(`span`,{style:{fontSize:14,fontWeight:700,'
        'color:_gu?`#0a0a0a`:`#64748b`,letterSpacing:`-0.01em`,textAlign:`center`},'
        'children:_gu||`tap to generate username`})]'
    )
    NEW_RAW = (
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
    if OLD_RAW in content:
        content = content.replace(OLD_RAW, NEW_RAW, 1)
        print('OK: signup bird fixed via raw match')
    else:
        errors.append('FAIL: broken signup bird block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
