#!/usr/bin/env python3
"""Patch v480 -> v482: Direct DOM mutation approach for ptr-strip color."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v480.js'
dst = '_deploy/assets/index-DUcNPOLc-v482.js'

content = open(src, encoding='utf-8').read()
errors = []

SET_GRAY = '(()=>{const _p=document.querySelector(`.ptr-strip`);if(_p)_p.style.background=`#1a1d27`;})()'
SET_DARK = '(()=>{const _p=document.querySelector(`.ptr-strip`);if(_p)_p.style.background=`#0b0f12`;})()'

OLD_PTR = 'zIndex:9999,background:`var(--ptr-bg,#0b0f12)`,pointerEvents:`none`'
NEW_PTR = 'zIndex:9999,background:`#0b0f12`,pointerEvents:`none`'
if OLD_PTR in content:
    content = content.replace(OLD_PTR, NEW_PTR, 1)
    print('OK: ptr-strip static')
else:
    errors.append('FAIL: ptr-strip')

OLD_OPEN = 'd(!0),document.documentElement.style.setProperty(`--ptr-bg`,`#1a1d27`)'
NEW_OPEN = f'd(!0),{SET_GRAY}'
if OLD_OPEN in content:
    content = content.replace(OLD_OPEN, NEW_OPEN, 1)
    print('OK: open')
else:
    errors.append('FAIL: open')

OLD_BD = 'onClick:()=>{l();document.documentElement.style.setProperty(`--ptr-bg`,`#0b0f12`)},'
NEW_BD = f'onClick:()=>{{l();{SET_DARK}}},'
if OLD_BD in content:
    content = content.replace(OLD_BD, NEW_BD, 1)
    print('OK: backdrop close')
else:
    errors.append('FAIL: backdrop close')

OLD_IN = 'if(e.target.tagName!==`A`&&e.target.tagName!==`BUTTON`&&e.target.tagName!==`IMG`){l();document.documentElement.style.setProperty(`--ptr-bg`,`#0b0f12`);}'
NEW_IN = f'if(e.target.tagName!==`A`&&e.target.tagName!==`BUTTON`&&e.target.tagName!==`IMG`){{l();{SET_DARK};}}'
if OLD_IN in content:
    content = content.replace(OLD_IN, NEW_IN, 1)
    print('OK: inner close')
else:
    errors.append('FAIL: inner close')

# view-post link still has bare onClick:l — wrap it
OLD_VP = 'to:`/post/${p}`,onClick:l,style:'
NEW_VP = f'to:`/post/${{p}}`,onClick:()=>{{l();{SET_DARK}}},style:'
if OLD_VP in content:
    content = content.replace(OLD_VP, NEW_VP, 1)
    print('OK: view-post close')
else:
    errors.append('FAIL: view-post close')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
