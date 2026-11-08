#!/usr/bin/env python3
"""Patch v305 -> v306: reliable iOS keyboard handling.
Reintroduce visualViewport listener but correctly:
- Listen to BOTH resize AND scroll events (iOS fires scroll, not just resize)
- 300ms debounce so panel only updates after keyboard animation finishes
- Store listener on window._dmSetVh for proper cleanup
- Panel uses var(--vvh, 100dvh) for height"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v305.js'
dst = '_deploy/assets/index-DUcNPOLc-v306.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add visualViewport listener to the if(_dmThread) block ────────────────
OLD_IF = (
    'if(_dmThread){let _sy=window.scrollY;'
    'document.body.style.overflow=`hidden`;'
    'document.body.style.position=`fixed`;'
    'document.body.style.top=`-${_sy}px`;'
    'document.body.style.width=`100%`;}'
)
NEW_IF = (
    'if(_dmThread){'
      'let _sy=window.scrollY;'
      'document.body.style.overflow=`hidden`;'
      'document.body.style.position=`fixed`;'
      'document.body.style.top=`-${_sy}px`;'
      'document.body.style.width=`100%`;'
      # Set initial height immediately (no debounce)
      'document.documentElement.style.setProperty(`--vvh`,(window.innerHeight)+`px`);'
      # Debounced listener — only fires after keyboard animation settles
      'let _vvT;'
      'const _fn=()=>{clearTimeout(_vvT);_vvT=setTimeout(()=>{'
        'const _h=window.visualViewport?window.visualViewport.height:window.innerHeight;'
        'document.documentElement.style.setProperty(`--vvh`,_h+`px`);'
      '},300);};'
      'window._dmSetVh=_fn;'
      'if(window.visualViewport){'
        'window.visualViewport.addEventListener(`resize`,_fn);'
        'window.visualViewport.addEventListener(`scroll`,_fn);'
      '}'
    '}'
)
if OLD_IF in content:
    content = content.replace(OLD_IF, NEW_IF, 1)
    print('OK: visualViewport debounced listener added to _dmThread effect')
else:
    errors.append('FAIL: scroll lock if block not found')

# ── 2. Add cleanup in the else block ─────────────────────────────────────────
OLD_ELSE = (
    '}else{let _sy=parseInt(document.body.style.top||`0`)*-1;'
    'document.body.style.overflow=``;'
    'document.body.style.position=``;'
    'document.body.style.top=``;'
    'document.body.style.width=``;'
    'window.scrollTo(0,_sy);}'
)
NEW_ELSE = (
    '}else{'
      'let _sy=parseInt(document.body.style.top||`0`)*-1;'
      'document.body.style.overflow=``;'
      'document.body.style.position=``;'
      'document.body.style.top=``;'
      'document.body.style.width=``;'
      'window.scrollTo(0,_sy);'
      'const _fn2=window._dmSetVh;'
      'if(_fn2&&window.visualViewport){'
        'window.visualViewport.removeEventListener(`resize`,_fn2);'
        'window.visualViewport.removeEventListener(`scroll`,_fn2);'
      '}'
      'window._dmSetVh=null;'
      'document.documentElement.style.removeProperty(`--vvh`);'
    '}'
)
if OLD_ELSE in content:
    content = content.replace(OLD_ELSE, NEW_ELSE, 1)
    print('OK: listener cleanup added to else block')
else:
    errors.append('FAIL: else block not found')

# ── 3. Add cleanup in the return (unmount) function ──────────────────────────
OLD_RETURN = (
    'return()=>{let _sy=parseInt(document.body.style.top||`0`)*-1;'
    'document.body.style.overflow=``;'
    'document.body.style.position=``;'
    'document.body.style.top=``;'
    'document.body.style.width=``;'
    'window.scrollTo(0,_sy);'
)
NEW_RETURN = (
    'return()=>{let _sy=parseInt(document.body.style.top||`0`)*-1;'
    'document.body.style.overflow=``;'
    'document.body.style.position=``;'
    'document.body.style.top=``;'
    'document.body.style.width=``;'
    'window.scrollTo(0,_sy);'
    'const _fn3=window._dmSetVh;'
    'if(_fn3&&window.visualViewport){'
      'window.visualViewport.removeEventListener(`resize`,_fn3);'
      'window.visualViewport.removeEventListener(`scroll`,_fn3);'
    '}'
    'window._dmSetVh=null;'
    'document.documentElement.style.removeProperty(`--vvh`);'
)
if OLD_RETURN in content:
    content = content.replace(OLD_RETURN, NEW_RETURN, 1)
    print('OK: listener cleanup added to return/unmount block')
else:
    errors.append('FAIL: return block not found')

# ── 4. Panel: use var(--vvh) so height tracks keyboard ───────────────────────
OLD_MOB = 'right:0,bottom:0,width:`100vw`,height:`100dvh`,background:`#13151c`'
NEW_MOB = 'right:0,bottom:0,width:`100vw`,height:`var(--vvh,100dvh)`,background:`#13151c`'
if OLD_MOB in content:
    content = content.replace(OLD_MOB, NEW_MOB, 1)
    print('OK: mobile DM panel uses var(--vvh)')
else:
    errors.append('FAIL: mobile panel height not found')

OLD_DESK = 'top:0,right:0,height:`100dvh`,width:`min(420px, 100vw)`'
NEW_DESK = 'top:0,right:0,height:`var(--vvh,100dvh)`,width:`min(420px, 100vw)`'
if OLD_DESK in content:
    content = content.replace(OLD_DESK, NEW_DESK, 1)
    print('OK: sidebar panel uses var(--vvh)')
else:
    errors.append('FAIL: sidebar panel height not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
