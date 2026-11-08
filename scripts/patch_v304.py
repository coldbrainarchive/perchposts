#!/usr/bin/env python3
"""Patch v303 -> v304:
1. Fix keyboard covering compose: use visualViewport resize to set --vvh CSS var,
   panel uses var(--vvh) so it always ends exactly where keyboard starts.
2. Fix reaction taps also triggering action sheet: add stopPropagation to reaction onClick."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v303.js'
dst = '_deploy/assets/index-DUcNPOLc-v304.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add visualViewport listener to body-scroll-lock useEffect ─────────────
# When _dmThread opens: lock body scroll AND track keyboard resize via visualViewport
OLD_SCROLL_LOCK = (
    'if(_dmThread){let _sy=window.scrollY;document.body.style.overflow=`hidden`;'
    'document.body.style.position=`fixed`;document.body.style.top=`-${_sy}px`;'
    'document.body.style.width=`100%`;}'
)
NEW_SCROLL_LOCK = (
    'if(_dmThread){'
      'let _sy=window.scrollY;'
      'document.body.style.overflow=`hidden`;'
      'document.body.style.position=`fixed`;'
      'document.body.style.top=`-${_sy}px`;'
      'document.body.style.width=`100%`;'
      # Set initial --vvh and listen for keyboard resize
      'const _vv=window.visualViewport;'
      'const _setVh=()=>document.documentElement.style.setProperty(`--vvh`,(_vv?_vv.height:window.innerHeight)+`px`);'
      '_setVh();'
      'if(_vv)_vv.addEventListener(`resize`,_setVh);'
    '}else{'
      'document.documentElement.style.removeProperty(`--vvh`);'
      'const _vv=window.visualViewport;'
      'if(_vv){const _noop=()=>{};_vv.removeEventListener(`resize`,_noop);}'
    '}'
)
# Need to replace just the if block, keep the else and return
OLD_FULL = (
    'if(_dmThread){let _sy=window.scrollY;document.body.style.overflow=`hidden`;'
    'document.body.style.position=`fixed`;document.body.style.top=`-${_sy}px`;'
    'document.body.style.width=`100%`;}else{'
)
NEW_FULL = (
    'if(_dmThread){'
      'let _sy=window.scrollY;'
      'document.body.style.overflow=`hidden`;'
      'document.body.style.position=`fixed`;'
      'document.body.style.top=`-${_sy}px`;'
      'document.body.style.width=`100%`;'
      'const _vv=window.visualViewport;'
      'const _setVh=()=>document.documentElement.style.setProperty(`--vvh`,(_vv?_vv.height:window.innerHeight)+`px`);'
      '_setVh();'
      'if(_vv)_vv.addEventListener(`resize`,_setVh);'
    '}else{'
)
if OLD_FULL in content:
    content = content.replace(OLD_FULL, NEW_FULL, 1)
    print('OK: visualViewport resize listener added to scroll-lock effect')
else:
    errors.append('FAIL: body scroll lock if block not found')

# ── 2. Panel: use var(--vvh) so it resizes with keyboard ─────────────────────
# Change both occurrences of height:`100dvh` in the panel spread
OLD_H1 = 'right:0,bottom:0,width:`100vw`,height:`100dvh`,background:`#13151c`'
NEW_H1 = 'right:0,bottom:0,width:`100vw`,height:`var(--vvh, 100dvh)`,background:`#13151c`'
if OLD_H1 in content:
    content = content.replace(OLD_H1, NEW_H1, 1)
    print('OK: mobile DM panel height uses var(--vvh)')
else:
    errors.append('FAIL: mobile panel height not found')

OLD_H2 = 'top:0,right:0,height:`100dvh`,width:`min(420px, 100vw)`'
NEW_H2 = 'top:0,right:0,height:`var(--vvh, 100dvh)`,width:`min(420px, 100vw)`'
if OLD_H2 in content:
    content = content.replace(OLD_H2, NEW_H2, 1)
    print('OK: desktop sidebar panel height uses var(--vvh)')
else:
    errors.append('FAIL: desktop panel height not found')

# ── 3. Fix reaction onClick: stopPropagation so bubble doesn't toggle actions ─
OLD_RX_CLICK = (
    'className:`chat-reaction-pill${_us.includes(_myUser)?` mine`:``}`,'
    'onClick:async()=>{await fetch(`${R}/dm-react`,'
)
NEW_RX_CLICK = (
    'className:`chat-reaction-pill${_us.includes(_myUser)?` mine`:``}`,'
    'onClick:async(e)=>{e.stopPropagation();await fetch(`${R}/dm-react`,'
)
if OLD_RX_CLICK in content:
    content = content.replace(OLD_RX_CLICK, NEW_RX_CLICK, 1)
    print('OK: reaction onClick gets stopPropagation — no more spurious action sheet toggle')
else:
    errors.append('FAIL: reaction onClick not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
