#!/usr/bin/env python3
"""Patch v302 -> v303: prevent iOS body scroll bleed-through.
When a DM thread opens, lock document.body so iOS Safari can't scroll
the underlying feed into view when the keyboard opens.
Restores scroll on close/unmount."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v302.js'
dst = '_deploy/assets/index-DUcNPOLc-v303.js'

content = open(src, encoding='utf-8').read()
errors = []

# Inject body-scroll-lock useEffect right after the _initDm useEffect
OLD_ANCHOR = 'if(!_initDm)return;l(`inbox`);_setDmThread(_initDm);},[_initDm]);(0,_.useEffect)'
NEW_ANCHOR = (
    'if(!_initDm)return;l(`inbox`);_setDmThread(_initDm);},[_initDm]);'
    # Body scroll lock: runs whenever _dmThread changes
    '(0,_.useEffect)(()=>{'
      'if(_dmThread){'
        'let _sy=window.scrollY;'
        'document.body.style.overflow=`hidden`;'
        'document.body.style.position=`fixed`;'
        'document.body.style.top=`-${_sy}px`;'
        'document.body.style.width=`100%`;'
      '}else{'
        'let _sy=parseInt(document.body.style.top||`0`)*-1;'
        'document.body.style.overflow=``;'
        'document.body.style.position=``;'
        'document.body.style.top=``;'
        'document.body.style.width=``;'
        'window.scrollTo(0,_sy);'
      '}'
      'return()=>{'
        'let _sy=parseInt(document.body.style.top||`0`)*-1;'
        'document.body.style.overflow=``;'
        'document.body.style.position=``;'
        'document.body.style.top=``;'
        'document.body.style.width=``;'
        'window.scrollTo(0,_sy);'
      '};'
    '},[_dmThread]);'
    '(0,_.useEffect)'
)
if OLD_ANCHOR in content:
    content = content.replace(OLD_ANCHOR, NEW_ANCHOR, 1)
    print('OK: body scroll lock useEffect injected')
else:
    errors.append('FAIL: _initDm useEffect anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
