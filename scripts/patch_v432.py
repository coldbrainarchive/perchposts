#!/usr/bin/env python3
"""Patch v431 -> v432:
Persist _adminUsers to localStorage so once borbie is seen as admin anywhere,
every future page load knows immediately — no more teal flash or wrong chip.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v431.js'
dst = '_deploy/assets/index-DUcNPOLc-v432.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace empty Set init with localStorage-backed init + helper fn ───────
OLD_SET = 'var _jailed=new Set(),_banned=new Set(),_adminUsers=new Set();'
NEW_SET = (
    'var _jailed=new Set(),_banned=new Set();'
    'var _adminUsers=(()=>{try{return new Set(JSON.parse(localStorage.getItem(`_au`)||`[]`));}catch(_){return new Set();}})();'
    'function _addAdmin(u){if(!u)return;const l=u.toLowerCase();if(_adminUsers.has(l))return;_adminUsers.add(l);try{const c=JSON.parse(localStorage.getItem(`_au`)||`[]`);c.push(l);localStorage.setItem(`_au`,JSON.stringify(c));}catch(_){}}'
)
if OLD_SET in content:
    content = content.replace(OLD_SET, NEW_SET, 1)
    print('OK: _adminUsers initialised from localStorage + _addAdmin helper')
else:
    errors.append('FAIL: Set declarations not found')

# ── 2. Replace _adminUsers.add() calls with _addAdmin() ──────────────────────
replacements = [
    ('if(e.username)_adminUsers.add(e.username.toLowerCase())',
     'if(e.username)_addAdmin(e.username)'),
    ('if(_u.role===`admin`&&_u.username)_adminUsers.add(_u.username.toLowerCase())',
     'if(_u.role===`admin`&&_u.username)_addAdmin(_u.username)'),
    ('if(_ua?.role===`admin`)_adminUsers.add(m.toLowerCase())',
     'if(_ua?.role===`admin`)_addAdmin(m)'),
]
for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'OK: replaced {old[:50]}...')
    else:
        errors.append(f'FAIL: not found: {old[:60]}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
