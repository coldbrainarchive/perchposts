#!/usr/bin/env python3
"""Patch v131 -> v132: bigger signup bird + multi-hue drop-shadow spots for ~2/3 of users."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v131.js'
dst = '_deploy/assets/index-DUcNPOLc-v132.js'

content = open(src, encoding='utf-8').read()
errors = []

# Shared JS that builds the full filter string from a username string
# Returns: hue-rotate + optional coloured drop-shadows (spots)
FILTER_FN = (
    '(function(_s){'
    'var _h=0;'
    'for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
    'var _a=Math.abs(_h);'
    'var _f=`hue-rotate(${_a%360}deg)`;'
    # ~67% of users get spots (skip only when _a%3===0)
    'if(_a%3!==0){'
    'var _h1=(_a*7+137)%360;'
    'var _h2=(_a*13+251)%360;'
    'var _ox1=((_a>>4)%5)+2;'    # 2-6px offset
    'var _oy1=-((_a>>7)%5)-2;'   # -2 to -6px
    'var _ox2=-((_a>>10)%4)-1;'  # -1 to -4px
    'var _oy2=((_a>>13)%4)+2;'   # 2-5px
    'if(_a%3===1){'
    # One spot
    '_f+=` drop-shadow(${_ox1}px ${_oy1}px 0px hsl(${_h1},90%,58%))`;'
    '}else{'
    # Two spots
    '_f+=` drop-shadow(${_ox1}px ${_oy1}px 0px hsl(${_h1},90%,58%))'
    ' drop-shadow(${_ox2}px ${_oy2}px 0px hsl(${_h2},90%,58%))`;'
    '}'
    '}'
    'return _f'
    '})'
)

# 1. Update Jn: return {e, f} where f is the full filter string
OLD_JN = (
    'return{e:`🐤`,h:(function(_s){var _h=0;for(var _i=0;_i<_s.length;_i++)'
    '_h=_s.charCodeAt(_i)+((_h<<5)-_h);return Math.abs(_h)%360})(_s)}'
)
NEW_JN = f'return{{e:`🐤`,f:{FILTER_FN}(_s)}}'

if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: Jn returns full filter string with optional spots')
else:
    errors.append('FAIL: Jn return not found')

# 2. Update badge render: use i.f instead of i.h
OLD_BADGE = (
    'style:typeof i===`object`?{filter:`hue-rotate(${i.h}deg)`,display:`inline-block`}:{}'
)
NEW_BADGE = (
    'style:typeof i===`object`?{filter:i.f,display:`inline-block`}:{}'
)
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: badge uses full filter string')
else:
    errors.append('FAIL: badge style not found')

# 3. Signup bird: bigger (36px) + full filter with spots
OLD_SIGNUP = (
    'position:`absolute`,left:12,fontSize:18,lineHeight:1,'
    'filter:_gu?`hue-rotate(${  (function(_s){var _h=0;for(var _i=0;_i<_s.length;_i++)'
    '_h=_s.charCodeAt(_i)+((_h<<5)-_h);return Math.abs(_h)%360})(_gu)  }deg)`:``'
)
NEW_SIGNUP = (
    f'position:`absolute`,left:12,fontSize:36,lineHeight:1,'
    f'filter:_gu?{FILTER_FN}(_gu):``'
)
if OLD_SIGNUP in content:
    content = content.replace(OLD_SIGNUP, NEW_SIGNUP, 1)
    print('OK: signup bird 36px + full filter with spots')
else:
    errors.append('FAIL: signup bird not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
