#!/usr/bin/env python3
"""Patch v105 -> v106: fix Safari TDZ 'Cannot access e before initialization'.

Wr component has {user:e} as prop. Two inner arrow functions also use 'e' as
a let/catch binding (useEffect let e=Gn() and catch(e) in F), which triggers
Safari/JSC's closure-TDZ bug when e is accessed via closure in F's success path.
Fix: rename both inner 'e' bindings to avoid the collision.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v105.js'
dst = '_deploy/assets/index-DUcNPOLc-v106.js'

content = open(src, encoding='utf-8').read()
errors = []

# Fix 1: let e=Gn() in check-jailed useEffect -> let _bid=Gn()
OLD_UE = '(0,_.useEffect)(()=>{if(N)return;let e=Gn();fetch(`${R}/check-jailed?browser_id=${e}`).then(e=>e.json()).then(e=>{e.jailed&&se(!0)}).catch(()=>{})},[N]);'
NEW_UE = '(0,_.useEffect)(()=>{if(N)return;let _bid=Gn();fetch(`${R}/check-jailed?browser_id=${_bid}`).then(e=>e.json()).then(e=>{e.jailed&&se(!0)}).catch(()=>{})},[N]);'
if OLD_UE in content:
    content = content.replace(OLD_UE, NEW_UE, 1)
    print('OK: renamed let e=Gn() -> let _bid=Gn() in check-jailed useEffect')
else:
    errors.append('FAIL: check-jailed useEffect let e not found')

# Fix 2: catch(e) in F comment handler -> catch(_ce)
OLD_CATCH = '}catch(e){v(e=>e.filter(e=>e.id!==a)),h(!1),console.error(e)}'
NEW_CATCH = '}catch(_ce){v(e=>e.filter(e=>e.id!==a)),h(!1),console.error(_ce)}'
if OLD_CATCH in content:
    content = content.replace(OLD_CATCH, NEW_CATCH, 1)
    print('OK: renamed catch(e) -> catch(_ce) in F comment handler')
else:
    errors.append('FAIL: catch(e) in F not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
