#!/usr/bin/env python3
"""Patch v554 -> v555:
- Add swipe detection to global pill click handler (skip if finger moved > 8px)
- Only show global overlay when _gpStats is loaded (condition: _gpBird && _gpStats)
- On fetch error, fail silently instead of opening a blank overlay
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v554.js'
dst = '_deploy/assets/index-DUcNPOLc-v555.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add swipe detection + tighten click handler ───────────────────────────
OLD_HANDLER = ('const _hgpb=ev=>{'
               'const el=ev.target.closest(`[data-gpb]`);'
               'if(!el)return;'
               'const un=el.getAttribute(`data-gpb`);'
               'if(!un||un.includes(`#`))return;'
               'if(ev.target.closest(`button`))return;'
               'ev.stopPropagation();'
               'fetch(`${R}/user-stats?username=${encodeURIComponent(un)}`)'
               '.then(r=>r.json())'
               '.then(d=>{_setGpStats(d);_setGpBird(un);})'
               '.catch(()=>_setGpBird(un));'
               '};'
               'document.addEventListener(`click`,_hgpb,!0);'
               'return window.addEventListener(`like-no-auth`,e),'
               'window.addEventListener(`open-dm`,_odm),'
               '()=>{window.removeEventListener(`like-no-auth`,e);'
               'window.removeEventListener(`open-dm`,_odm);'
               'document.removeEventListener(`click`,_hgpb,!0)}')
NEW_HANDLER = ('let _gpbMoved=!1,_gpbTX=0,_gpbTY=0;'
               'const _gpbTS=ev=>{_gpbTX=ev.touches[0].clientX;_gpbTY=ev.touches[0].clientY;_gpbMoved=!1;};'
               'const _gpbTM=ev=>{if(Math.abs(ev.touches[0].clientX-_gpbTX)>8||Math.abs(ev.touches[0].clientY-_gpbTY)>8)_gpbMoved=!0;};'
               'const _hgpb=ev=>{'
               'if(_gpbMoved)return;'
               'const el=ev.target.closest(`[data-gpb]`);'
               'if(!el)return;'
               'const un=el.getAttribute(`data-gpb`);'
               'if(!un||un.includes(`#`))return;'
               'if(ev.target.closest(`button`))return;'
               'ev.stopPropagation();'
               'fetch(`${R}/user-stats?username=${encodeURIComponent(un)}`)'
               '.then(r=>r.json())'
               '.then(d=>{_setGpStats(d);_setGpBird(un);})'
               '.catch(()=>{});'
               '};'
               'document.addEventListener(`touchstart`,_gpbTS,{passive:!0});'
               'document.addEventListener(`touchmove`,_gpbTM,{passive:!0});'
               'document.addEventListener(`click`,_hgpb,!0);'
               'return window.addEventListener(`like-no-auth`,e),'
               'window.addEventListener(`open-dm`,_odm),'
               '()=>{window.removeEventListener(`like-no-auth`,e);'
               'window.removeEventListener(`open-dm`,_odm);'
               'document.removeEventListener(`touchstart`,_gpbTS);'
               'document.removeEventListener(`touchmove`,_gpbTM);'
               'document.removeEventListener(`click`,_hgpb,!0)}')
if OLD_HANDLER in content:
    content = content.replace(OLD_HANDLER, NEW_HANDLER, 1)
    print('OK: swipe detection + silent error added')
else:
    errors.append('FAIL: global click handler not found')

# ── 2. Only render global overlay when _gpStats is loaded ────────────────────
OLD_COND = '_gpBird?(0,L.jsxs)(`div`,{onClick:()=>{_setGpBird(null);_setGpStats(null);}'
NEW_COND = '_gpBird&&_gpStats?(0,L.jsxs)(`div`,{onClick:()=>{_setGpBird(null);_setGpStats(null);}'
if OLD_COND in content:
    content = content.replace(OLD_COND, NEW_COND, 1)
    print('OK: overlay gated on _gpStats loaded')
else:
    errors.append('FAIL: global overlay condition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
