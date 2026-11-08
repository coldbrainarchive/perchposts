#!/usr/bin/env python3
"""Patch v183 -> v184: check-role poll — auto sign-out on demotion."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v183.js'
dst = '_deploy/assets/index-DUcNPOLc-v184.js'

content = open(src, encoding='utf-8').read()
errors = []

# Inject check-role useEffect after the user-stats effect in Kr.
# The user-stats effect ends with: ...},[e,r,k]);
# We target the specific closing of that effect then inject immediately after.
OLD = '_shd(`${dd}-${mm}-${yy}`);}}})();},[e,r,k]);let re=async()'
NEW = (
    '_shd(`${dd}-${mm}-${yy}`);}}})();},[e,r,k]);'
    # Check-role poll: every 30s, auto-logout if demoted
    '(0,_.useEffect)(()=>{'
    'if(!e)return;'
    'const _cr=async()=>{try{'
    'let _n=await fetch(`${R}/check-role`,{headers:er()});'
    'if(_n.ok){let _d=await _n.json();if(_d.role_mismatch)o();}'
    '}catch(_){}};'
    '_cr();'
    'const _ci=setInterval(_cr,30000);'
    'return()=>clearInterval(_ci);'
    '},[e]);'
    'let re=async()'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: check-role poll injected in Kr')
else:
    errors.append('FAIL: user-stats effect tail not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
