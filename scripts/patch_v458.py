#!/usr/bin/env python3
"""Patch v457 -> v458:
Replace the 4-frame RAF retry (which creates a iOS cursor feedback loop) with a
MutationObserver on the dropdown. The observer fires at the exact moment user
pills are inserted into the DOM, then restores cursor ONCE in a single RAF.
This avoids the loop: observer disconnects itself before the RAF fires.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v457.js'
dst = '_deploy/assets/index-DUcNPOLc-v458.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Give the dropdown an id so MutationObserver can target it ─────────────
OLD_DD = '(E&&(S||C||P||w||T||UR.length>0))&&(0,L.jsxs)(`div`,{className:`search-dropdown`,'
NEW_DD = '(E&&(S||C||P||w||T||UR.length>0))&&(0,L.jsxs)(`div`,{className:`search-dropdown`,id:`_urd`,'
if OLD_DD in content:
    content = content.replace(OLD_DD, NEW_DD, 1)
    print('OK: dropdown given id=_urd')
else:
    errors.append('FAIL: dropdown condition not found')

# ── 2. Replace 4-frame retry with MutationObserver ───────────────────────────
OLD_CR = ('const _sc=c.current?c.current.selectionStart:null;'
          'r(_sv);'
          'if(_sc!==null){let _t=4;const _rf=()=>{if(_t-->0&&c.current&&document.activeElement===c.current)'
          '{c.current.setSelectionRange(_sc,_sc);requestAnimationFrame(_rf);}};requestAnimationFrame(_rf);}')
NEW_CR = ('const _sc=c.current?c.current.selectionStart:null;'
          'r(_sv);'
          'if(_sc!==null){'
          'const _urd=document.getElementById(`_urd`);'
          'if(_urd){'
          'if(c.current._mo){c.current._mo.disconnect();}'
          'c.current._mo=new MutationObserver(()=>{'
          'if(c.current._mo){c.current._mo.disconnect();c.current._mo=null;}'
          'if(c.current&&document.activeElement===c.current)'
          'requestAnimationFrame(()=>{'
          'if(c.current&&document.activeElement===c.current)'
          'c.current.setSelectionRange(_sc,_sc);});});'
          'c.current._mo.observe(_urd,{childList:true,subtree:true});'
          'setTimeout(()=>{if(c.current&&c.current._mo){c.current._mo.disconnect();c.current._mo=null;}},2000);}}')
if OLD_CR in content:
    content = content.replace(OLD_CR, NEW_CR, 1)
    print('OK: cursor restore replaced with MutationObserver approach')
else:
    errors.append('FAIL: 4-frame retry code not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
