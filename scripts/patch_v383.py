#!/usr/bin/env python3
"""Patch v382 -> v383:
- Add _postNotFound state to Wr
- Set it when get-post returns non-ok (404, deleted, etc.)
- Show friendly placeholder instead of blank page
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v382.js'
dst = '_deploy/assets/index-DUcNPOLc-v383.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _postNotFound state next to _huddleDenied ──────────────────────────
OLD_STATE = '[_huddleDenied,_setHuddleDenied]=(0,_.useState)(!1),'
NEW_STATE = '[_huddleDenied,_setHuddleDenied]=(0,_.useState)(!1),[_postNotFound,_setPostNotFound]=(0,_.useState)(!1),'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _postNotFound state added')
else:
    errors.append('FAIL: Wr state not found')

# ── 2. Set _postNotFound when P() gets a non-ok response ──────────────────────
OLD_P_ERR = 'if(!e.ok)return;let{post:t,comments:n}=await e.json()'
NEW_P_ERR = 'if(!e.ok){_setPostNotFound(!0);return;}let{post:t,comments:n}=await e.json()'
if OLD_P_ERR in content:
    content = content.replace(OLD_P_ERR, NEW_P_ERR, 1)
    print('OK: P() sets _postNotFound on error')
else:
    errors.append('FAIL: P() error return not found')

# ── 3. Add not-found placeholder before the huddle-denied placeholder ──────────
OLD_DENIED = 'if(_huddleDenied)return(0,L.jsx)(`div`'
NEW_DENIED = (
    'if(_postNotFound)return(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,padding:40,textAlign:`center`,color:`#94a3b8`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:12},children:`🔍`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:16,fontWeight:700,color:`#f8fafc`,marginBottom:6},children:`Post not found`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:13},children:`This post may have been deleted or is no longer available.`}),'
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>{window.location.href=`/`;},style:{marginTop:20,padding:`8px 20px`,borderRadius:8,border:`1px solid #374151`,background:`none`,color:`#94a3b8`,cursor:`pointer`,fontSize:13},children:`Go home`})]});'
    'if(_huddleDenied)return(0,L.jsx)(`div`'
)
if OLD_DENIED in content:
    content = content.replace(OLD_DENIED, NEW_DENIED, 1)
    print('OK: post-not-found placeholder added')
else:
    errors.append('FAIL: _huddleDenied render not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
