#!/usr/bin/env python3
"""Patch v130 -> v131: unique hue-rotated 🐤 per user based on username hash."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v130.js'
dst = '_deploy/assets/index-DUcNPOLc-v131.js'

content = open(src, encoding='utf-8').read()
errors = []

# Helper JS snippet that computes a hue from a string (same pattern as Hn)
# Returns degrees 0-359
HUE_FN = (
    '(function(_s){'
    'var _h=0;for(var _i=0;_i<_s.length;_i++)_h=_s.charCodeAt(_i)+((_h<<5)-_h);'
    'return Math.abs(_h)%360'
    '})'
)

# 1. Update Jn: return object {e:'🐤', h: hue} for regular users
OLD_JN = (
    'function Jn(e){if(!e)return null;'
    'if(e.username&&_jailed.has(e.username))return`\U0001fab9`;'
    'if(e.username&&_banned.has(e.username))return`❌`;'
    'return e.browser_id&&String(e.browser_id).startsWith(`bot-`)?`🤖`:e.is_admin?`🐧`:e.is_mod?`🐦`:e.username?`🐤`:null}'
)
NEW_JN = (
    'function Jn(e){if(!e)return null;'
    'if(e.username&&_jailed.has(e.username))return`\U0001fab9`;'
    'if(e.username&&_banned.has(e.username))return`❌`;'
    'if(e.browser_id&&String(e.browser_id).startsWith(`bot-`))return`🤖`;'
    'if(e.is_admin)return`🐧`;'
    'if(e.is_mod)return`🐦`;'
    'var _s=e.username||(e.browser_id||``).slice(0,8);'
    'if(!_s)return null;'
    f'return{{e:`🐤`,h:{HUE_FN}(_s)}}'
    '}'
)
if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: Jn returns hue object for regular users')
else:
    errors.append('FAIL: Jn not found')

# 2. Update badge rendering in Xn to handle the {e, h} object
OLD_BADGE = 'i&&(0,L.jsx)(`span`,{className:`user-pill-badge`,children:i})'
NEW_BADGE = (
    'i&&(0,L.jsx)(`span`,{className:`user-pill-badge`,'
    'style:typeof i===`object`?{filter:`hue-rotate(${i.h}deg)`,display:`inline-block`}:{},'
    'children:typeof i===`object`?i.e:i})'
)
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: badge renders with hue-rotate filter')
else:
    errors.append('FAIL: badge render not found')

# 3. Update signup pill 🐤 to use hue based on _gu
OLD_BIRD = 'position:`absolute`,left:12,fontSize:18,lineHeight:1},children:`🐤`}'
NEW_BIRD = (
    'position:`absolute`,left:12,fontSize:18,lineHeight:1,'
    f'filter:_gu?`hue-rotate(${{  {HUE_FN}(_gu)  }}deg)`:``'
    '},children:`🐤`}'
)
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: signup 🐤 hue-rotated from generated username')
else:
    errors.append('FAIL: signup bird not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
