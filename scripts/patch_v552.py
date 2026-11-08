#!/usr/bin/env python3
"""Patch v551 -> v552:
Fix global pill click handler — if pill is inside a <button>, skip overlay
so button's own onClick (e.g. search filter clear, nav panel open) fires normally.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v551.js'
dst = '_deploy/assets/index-DUcNPOLc-v552.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_HANDLER = ('const _hgpb=ev=>{'
               'const el=ev.target.closest(`[data-gpb]`);'
               'if(!el)return;'
               'const un=el.getAttribute(`data-gpb`);'
               'if(!un||un.includes(`#`))return;'
               'ev.stopPropagation();'
               '_setGpBird(un);'
               '};')
NEW_HANDLER = ('const _hgpb=ev=>{'
               'const el=ev.target.closest(`[data-gpb]`);'
               'if(!el)return;'
               'const un=el.getAttribute(`data-gpb`);'
               'if(!un||un.includes(`#`))return;'
               'if(ev.target.closest(`button`))return;'
               'ev.stopPropagation();'
               '_setGpBird(un);'
               '};')

if OLD_HANDLER in content:
    content = content.replace(OLD_HANDLER, NEW_HANDLER, 1)
    print('OK: button exclusion added to pill click handler')
else:
    errors.append('FAIL: pill click handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
