#!/usr/bin/env python3
"""Patch v137 -> v139: add coloured spots on top of bird emoji (fix injection point)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v137.js'
dst = '_deploy/assets/index-DUcNPOLc-v139.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Inject _mkSpots + _spEls AFTER _mkBird's closing } ────────────────────
# '}var e=Object.create' — the } closes _mkBird; inject AFTER it
INJECT_MARKER = '}var e=Object.create'
SPOTS_FNS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%5*0.1+0.18,y:(sv>>6)%4*0.1+0.3,w:(sv>>9)%2*0.08+0.18});}'
    'return spots;}'
    'function _spEls(spots,sz){'
    "return(spots||[]).map(function(s,i){"
    "return(0,L.jsx)('span',{style:{position:'absolute',borderRadius:'50%',"
    "background:`hsl(${s.h},82%,62%)`,width:sz*s.w+'px',height:sz*s.w+'px',"
    "left:sz*s.x+'px',top:sz*s.y+'px',pointerEvents:'none',opacity:0.8,zIndex:1}},i);});}"
)

if INJECT_MARKER in content:
    # Replace '}var e=...' with '}' + new fns + 'var e=...' so fns land at module level
    content = content.replace(INJECT_MARKER, '}' + SPOTS_FNS + 'var e=Object.create', 1)
    print('OK: _mkSpots + _spEls injected at module level after _mkBird')
else:
    errors.append('FAIL: _mkBird end / inject point not found')

# ── 2. Update Jn return to include spots ─────────────────────────────────────
OLD_JN_RETURN = 'return{e:_e,f:_f}}'
NEW_JN_RETURN = 'return{e:_e,f:_f,s:_mkSpots(_a)}}'

if OLD_JN_RETURN in content:
    content = content.replace(OLD_JN_RETURN, NEW_JN_RETURN, 1)
    print('OK: Jn return updated to include spots')
else:
    errors.append('FAIL: Jn return not found')

# ── 3. Update badge render to show spots on top ───────────────────────────────
OLD_BADGE = (
    'i&&(0,L.jsx)(`span`,{className:`user-pill-badge`,'
    'style:typeof i===`object`&&i.f?{filter:i.f,display:`inline-block`}:{},'
    'children:typeof i===`object`&&i.e?i.e:i})'
)
NEW_BADGE = (
    'i&&(0,L.jsxs)(`span`,{className:`user-pill-badge`,'
    'style:{position:`relative`,display:`inline-block`},'
    'children:['
    '(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[])'
    ']})'
)

if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: badge render updated with spots')
else:
    errors.append('FAIL: badge render not found')

# ── 4. Update signup bird to show spots ──────────────────────────────────────
OLD_SIGNUP_RETURN = (
    'return(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:40,'
    'lineHeight:1,filter:_f},children:_e})'
)
NEW_SIGNUP_RETURN = (
    'var _sp=_mkSpots(_a);'
    'return(0,L.jsxs)(`span`,{style:{position:`absolute`,left:12,fontSize:40,'
    'lineHeight:1,display:`inline-block`},'
    'children:['
    '(0,L.jsx)(`span`,{style:{filter:_f},children:_e}),'
    '..._spEls(_sp,40)'
    ']})'
)

if OLD_SIGNUP_RETURN in content:
    content = content.replace(OLD_SIGNUP_RETURN, NEW_SIGNUP_RETURN, 1)
    print('OK: signup bird updated with spots')
else:
    errors.append('FAIL: signup bird return not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
