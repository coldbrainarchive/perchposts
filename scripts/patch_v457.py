#!/usr/bin/env python3
"""Patch v456 -> v457:
1. Hide dropdown when it has no content (was showing as a thin strip when
   typing text with no matching boards/regions/users).
   Gate on (S||C||P||w||T||UR.length>0) in addition to E.
2. Retry cursor restore 4 times across RAF frames so iOS can't win the race.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v456.js'
dst = '_deploy/assets/index-DUcNPOLc-v457.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add content guard to dropdown condition ────────────────────────────────
OLD_DD = 'E&&(0,L.jsxs)(`div`,{className:`search-dropdown`,'
NEW_DD = '(E&&(S||C||P||w||T||UR.length>0))&&(0,L.jsxs)(`div`,{className:`search-dropdown`,'
if OLD_DD in content:
    content = content.replace(OLD_DD, NEW_DD, 1)
    print('OK: dropdown gated on having content')
else:
    errors.append('FAIL: dropdown condition not found')

# ── 2. More aggressive cursor restore (4-frame retry loop) ────────────────────
OLD_CR = ('const _sc=c.current?c.current.selectionStart:null;'
          'r(_sv);'
          'if(_sc!==null)requestAnimationFrame(()=>requestAnimationFrame(()=>'
          '{if(c.current&&document.activeElement===c.current)'
          'c.current.setSelectionRange(_sc,_sc);}));')
NEW_CR = ('const _sc=c.current?c.current.selectionStart:null;'
          'r(_sv);'
          'if(_sc!==null){let _t=4;'
          'const _rf=()=>{if(_t-->0&&c.current&&document.activeElement===c.current)'
          '{c.current.setSelectionRange(_sc,_sc);requestAnimationFrame(_rf);}};'
          'requestAnimationFrame(_rf);}')
if OLD_CR in content:
    content = content.replace(OLD_CR, NEW_CR, 1)
    print('OK: cursor restore upgraded to 4-frame retry loop')
else:
    errors.append('FAIL: cursor restore code not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
