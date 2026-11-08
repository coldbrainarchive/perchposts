#!/usr/bin/env python3
"""Patch v409 -> v410:
- Spinner container: match page bg (#16171d), vertically centre spinner in revealed space
- Fix stuck at halfway: add touchcancel handler + snap-back on any non-threshold release
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v409.js'
dst = '_deploy/assets/index-DUcNPOLc-v410.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Spinner container: matching background, centred in revealed space ───────
OLD_SPIN_STYLE = (
    'position:`fixed`,top:0,left:0,right:0,height:60,zIndex:9999,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,'
    'paddingTop:12,pointerEvents:`none`}'
)
NEW_SPIN_STYLE = (
    'position:`fixed`,top:0,left:0,right:0,height:60,zIndex:9999,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,'
    'background:`#16171d`,pointerEvents:`none`}'
)
if OLD_SPIN_STYLE in content:
    content = content.replace(OLD_SPIN_STYLE, NEW_SPIN_STYLE, 1)
    print('OK: spinner container has matching background + centred')
else:
    errors.append('FAIL: spinner style not found')

# ── 2. Fix stuck: add touchcancel handler, snap back immediately ───────────────
OLD_EVENTS = (
    'document.addEventListener(`touchstart`,e,{passive:!0}),'
    'document.addEventListener(`touchmove`,t,{passive:!1}),'
    'document.addEventListener(`touchend`,n),'
    '()=>{document.removeEventListener(`touchstart`,e),'
    'document.removeEventListener(`touchmove`,t),'
    'document.removeEventListener(`touchend`,n)}'
)
NEW_EVENTS = (
    'document.addEventListener(`touchstart`,e,{passive:!0}),'
    'document.addEventListener(`touchmove`,t,{passive:!1}),'
    'document.addEventListener(`touchend`,n),'
    'document.addEventListener(`touchcancel`,n),'
    '()=>{document.removeEventListener(`touchstart`,e),'
    'document.removeEventListener(`touchmove`,t),'
    'document.removeEventListener(`touchend`,n),'
    'document.removeEventListener(`touchcancel`,n)}'
)
if OLD_EVENTS in content:
    content = content.replace(OLD_EVENTS, NEW_EVENTS, 1)
    print('OK: touchcancel handler added to fix stuck state')
else:
    errors.append('FAIL: event listeners not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
