#!/usr/bin/env python3
"""Patch v110 -> v111: reliable cage detection + instant cage UI.

Changes:
1. Init p (caged) and h (board) from localStorage so cage UI shows instantly
   on SPA navigation without waiting for async fetch.
2. Restructure Ur useEffect: fetch my-username FIRST, then check-jailed with
   both browser_id AND username so jail-by-username is caught client-side.
3. Cache jailed result in localStorage so subsequent visits are instant.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v110.js'
dst = '_deploy/assets/index-DUcNPOLc-v111.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Init p and h from localStorage ────────────────────────────────────────
OLD_INIT = (
    '[d,f]=(0,_.useState)(null),'
    '[p,m]=(0,_.useState)(!1),'
    '[h,g]=(0,_.useState)(sr(i.get(`board`))?.slug||`random`)'
)
NEW_INIT = (
    '[d,f]=(0,_.useState)(null),'
    '[p,m]=(0,_.useState)(localStorage.getItem(`_caged`)===`1`),'
    '[h,g]=(0,_.useState)(localStorage.getItem(`_caged`)===`1`?`cage`:sr(i.get(`board`))?.slug||`random`)'
)
if OLD_INIT in content:
    content = content.replace(OLD_INIT, NEW_INIT, 1)
    print('OK: p and h init from localStorage')
else:
    errors.append('FAIL: p/h init pattern not found')

# ── 2. Restructure useEffect: username first, then check-jailed with both ─────
OLD_EFFECT = (
    'let t=Gn();(async()=>{'
    'let e=await fetch(`${R}/check-jailed?browser_id=${t}`);'
    '(e.ok?await e.json():{}).jailed&&(m(!0),g(`cage`));'
    'try{let e=await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/my-username`,{headers:er()});'
    'if(e.ok){let t=await e.json();t.username&&f(t.username)}}catch{}'
    '})()'
)
NEW_EFFECT = (
    'let t=Gn();(async()=>{'
    'let _un=null;'
    'try{let _r=await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/my-username`,{headers:er()});'
    'if(_r.ok){let _d=await _r.json();_d.username&&(f(_d.username),_un=_d.username)}}catch{}'
    'let _ce=await fetch(`${R}/check-jailed?browser_id=${t}`+(_un?`&username=${encodeURIComponent(_un)}`:``))'
    ';(await(_ce.ok?_ce.json():{})).jailed?'
    '(m(!0),g(`cage`),localStorage.setItem(`_caged`,`1`)):localStorage.removeItem(`_caged`)'
    '})()'
)
if OLD_EFFECT in content:
    content = content.replace(OLD_EFFECT, NEW_EFFECT, 1)
    print('OK: useEffect restructured with username-first + localStorage cache')
else:
    errors.append('FAIL: useEffect pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
