#!/usr/bin/env python3
"""Patch v517 -> v518: Make _modUsers in-memory only (no localStorage) to prevent stale purple."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v517.js'
dst = '_deploy/assets/index-DUcNPOLc-v518.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace _modUsers localStorage-backed init + _addMod with simple in-memory versions
OLD = ('var _modUsers=(()=>{try{return new Set(JSON.parse(localStorage.getItem(`_mu`)||`[]`));}catch(_){return new Set();}})();'
       'function _addMod(u){if(!u)return;const l=u.toLowerCase();if(_modUsers.has(l))return;_modUsers.add(l);try{const c=JSON.parse(localStorage.getItem(`_mu`)||`[]`);c.push(l);localStorage.setItem(`_mu`,JSON.stringify(c));}catch(_){}}')
NEW = ('var _modUsers=new Set();'
       'function _addMod(u){if(!u)return;_modUsers.add(u.toLowerCase());}')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: _modUsers is now in-memory only')
else:
    errors.append('FAIL: _modUsers localStorage block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
