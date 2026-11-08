#!/usr/bin/env python3
"""Patch v309 -> v310: fix comment compose sticky by guarding body scroll restore.
The else branch and return cleanup both call window.scrollTo(0,_sy) unconditionally.
When _dmThread was never set, _sy=0 and this scrolls the page to top every time
the panel opens, destroying the user's scroll position and breaking the compose sticky.
Fix: only restore if body.style.position === 'fixed' (i.e. DM was actually open)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v309.js'
dst = '_deploy/assets/index-DUcNPOLc-v310.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Guard the else block ───────────────────────────────────────────────────
OLD_ELSE = (
    '}else{let _sy=parseInt(document.body.style.top||`0`)*-1;'
    'document.body.style.overflow=``;document.body.style.position=``;'
    'document.body.style.top=``;document.body.style.width=``;window.scrollTo(0,_sy);'
)
NEW_ELSE = (
    '}else{if(document.body.style.position===`fixed`){'
      'let _sy=parseInt(document.body.style.top||`0`)*-1;'
      'document.body.style.overflow=``;document.body.style.position=``;'
      'document.body.style.top=``;document.body.style.width=``;'
      'window.scrollTo(0,_sy);}else{'
      'document.body.style.overflow=``;document.body.style.position=``;'
      'document.body.style.top=``;document.body.style.width=``;}'
)
if OLD_ELSE in content:
    content = content.replace(OLD_ELSE, NEW_ELSE, 1)
    print('OK: else block guarded — only restores scroll if body was actually locked')
else:
    errors.append('FAIL: else block not found')

# ── 2. Guard the return/unmount cleanup ──────────────────────────────────────
OLD_RETURN = (
    'return()=>{let _sy=parseInt(document.body.style.top||`0`)*-1;'
    'document.body.style.overflow=``;document.body.style.position=``;'
    'document.body.style.top=``;document.body.style.width=``;window.scrollTo(0,_sy);'
)
NEW_RETURN = (
    'return()=>{if(document.body.style.position===`fixed`){'
      'let _sy=parseInt(document.body.style.top||`0`)*-1;'
      'document.body.style.overflow=``;document.body.style.position=``;'
      'document.body.style.top=``;document.body.style.width=``;'
      'window.scrollTo(0,_sy);}else{'
      'document.body.style.overflow=``;document.body.style.position=``;'
      'document.body.style.top=``;document.body.style.width=``;}'
)
if OLD_RETURN in content:
    content = content.replace(OLD_RETURN, NEW_RETURN, 1)
    print('OK: return cleanup guarded — only restores scroll if body was actually locked')
else:
    errors.append('FAIL: return block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
