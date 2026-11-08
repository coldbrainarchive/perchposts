#!/usr/bin/env python3
"""Patch v421 -> v422:
Pass browser_id and role through the Huddle invite URL so the pre-filled
user pill shows the correct bird/background (admin white, top-hat, etc.)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v421.js'
dst = '_deploy/assets/index-DUcNPOLc-v422.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. _UserCard button: pass _br record alongside username ───────────────────
OLD_BTN = 'onClick:()=>_om(_un),style:{width:`100%`'
NEW_BTN = 'onClick:()=>_om(_un,_br),style:{width:`100%`'
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: Huddle button passes _br record')
else:
    errors.append('FAIL: Huddle button onClick not found')

# ── 2. onMessage handler: encode browser_id and admin flag in URL ─────────────
OLD_OM = 'onMessage:(_u)=>{window.location.href=`/new?huddle=1&invite=${encodeURIComponent(_u)}`;}'
NEW_OM = 'onMessage:(_u,_rec)=>{let _hu=`/new?huddle=1&invite=${encodeURIComponent(_u)}`;if(_rec?.browser_id)_hu+=`&invite_bid=${encodeURIComponent(_rec.browser_id)}`;if(_rec?.is_admin)_hu+=`&invite_admin=1`;window.location.href=_hu;}'
if OLD_OM in content:
    content = content.replace(OLD_OM, NEW_OM, 1)
    print('OK: onMessage encodes browser_id + admin flag')
else:
    errors.append('FAIL: onMessage handler not found')

# ── 3. _hmTagged init: decode browser_id and role from URL params ─────────────
OLD_INV = 'const _inv=i.get(`invite`);return _inv?[{username:_inv}]:[];'
NEW_INV = 'const _inv=i.get(`invite`);if(!_inv)return[];const _ib=i.get(`invite_bid`)||null;const _ia=i.get(`invite_admin`)===`1`;return[{username:_inv,browser_id:_ib,role:_ia?`admin`:null}];'
if OLD_INV in content:
    content = content.replace(OLD_INV, NEW_INV, 1)
    print('OK: _hmTagged init reads browser_id + role from URL')
else:
    errors.append('FAIL: _hmTagged invite init not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
