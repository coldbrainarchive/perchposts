#!/usr/bin/env python3
"""Patch v455 -> v456:
1. Revert always-render dropdown back to conditional (E&&...) — the always-render
   caused an empty dropdown strip when there are no results.
2. Add cursor save/restore around the debounced r() call. After r() triggers a
   re-render (dropdown appears/changes), iOS Safari sometimes resets the cursor.
   We read selectionStart immediately before r() fires, then restore it two
   animation frames later (after React has committed and browser has painted).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v455.js'
dst = '_deploy/assets/index-DUcNPOLc-v456.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Revert always-render dropdown back to conditional ─────────────────────
OLD_DR = '(0,L.jsxs)(`div`,{className:`search-dropdown`,style:{display:E?`block`:`none`},'
NEW_DR = 'E&&(0,L.jsxs)(`div`,{className:`search-dropdown`,'
if OLD_DR in content:
    content = content.replace(OLD_DR, NEW_DR, 1)
    print('OK: dropdown back to conditional render')
else:
    errors.append('FAIL: always-render dropdown not found')

# ── 2. Add cursor save/restore around debounced r() ──────────────────────────
OLD_CB = 'c.current._dbt=setTimeout(()=>r(_sv),250);'
NEW_CB = ('c.current._dbt=setTimeout(()=>{'
          'const _sc=c.current?c.current.selectionStart:null;'
          'r(_sv);'
          'if(_sc!==null)requestAnimationFrame(()=>requestAnimationFrame(()=>{'
          'if(c.current&&document.activeElement===c.current)'
          'c.current.setSelectionRange(_sc,_sc);}));'
          '},250);')
if OLD_CB in content:
    content = content.replace(OLD_CB, NEW_CB, 1)
    print('OK: cursor save/restore added around debounced r()')
else:
    errors.append('FAIL: debounced setTimeout callback not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
