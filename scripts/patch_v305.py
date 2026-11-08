#!/usr/bin/env python3
"""Patch v304 -> v305: revert visualViewport JS listener — it was causing the panel to
shrink to the wrong height during keyboard animation. iOS handles 100dvh correctly on
its own. Remove the --vvh CSS variable approach, restore plain 100dvh on the panel."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v304.js'
dst = '_deploy/assets/index-DUcNPOLc-v305.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove visualViewport listener from body scroll lock effect ────────────
OLD_VV = (
    'document.body.style.width=`100%`;'
    'const _vv=window.visualViewport;'
    'const _setVh=()=>document.documentElement.style.setProperty(`--vvh`,(_vv?_vv.height:window.innerHeight)+`px`);'
    '_setVh();if(_vv)_vv.addEventListener(`resize`,_setVh);'
)
NEW_VV = 'document.body.style.width=`100%`;'
if OLD_VV in content:
    content = content.replace(OLD_VV, NEW_VV, 1)
    print('OK: visualViewport listener removed')
else:
    errors.append('FAIL: visualViewport block not found')

# ── 2. Revert panel height from var(--vvh) back to 100dvh (mobile full-screen) ─
OLD_H_MOB = 'width:`100vw`,height:`var(--vvh, 100dvh)`,background:`#13151c`'
NEW_H_MOB = 'width:`100vw`,height:`100dvh`,background:`#13151c`'
if OLD_H_MOB in content:
    content = content.replace(OLD_H_MOB, NEW_H_MOB, 1)
    print('OK: mobile DM panel reverted to height:100dvh')
else:
    errors.append('FAIL: mobile panel var(--vvh) not found')

# ── 3. Revert sidebar panel height too ───────────────────────────────────────
OLD_H_DESK = 'top:0,right:0,height:`var(--vvh, 100dvh)`,width:`min(420px, 100vw)`'
NEW_H_DESK = 'top:0,right:0,height:`100dvh`,width:`min(420px, 100vw)`'
if OLD_H_DESK in content:
    content = content.replace(OLD_H_DESK, NEW_H_DESK, 1)
    print('OK: sidebar panel reverted to height:100dvh')
else:
    errors.append('FAIL: sidebar panel var(--vvh) not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
