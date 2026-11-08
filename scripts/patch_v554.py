#!/usr/bin/env python3
"""Patch v553 -> v554:
Fetch /user-stats BEFORE opening either Bird overlay so the card and buttons
render together in one paint instead of two.
Changes:
  A. _UserCard accepts optional `stats` prop — skips fetch if provided
  B. qr() global overlay: fetch stats on pill click, set _gpStats + _gpBird together
     - Add _gpStats state; pass stats to _UserCard; clear on close
  C. Rr comment overlay: fetch stats on Bird tap, set _birdStats + _birdOpen together
     - Add _birdStats state; pass stats to _UserCard; clear on close
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v553.js'
dst = '_deploy/assets/index-DUcNPOLc-v554.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── A. _UserCard: accept stats prop, skip fetch if provided ──────────────────
OLD_UC_DEF = ('function _UserCard({username:_un,onMessage:_om,record:_br})'
              '{const[_s,_ss]=(0,_.useState)(null);'
              '(0,_.useEffect)(()=>{if(!_un)return;'
              'fetch(`${R}/user-stats?username=${encodeURIComponent(_un)}`)'
              '.then(r=>r.json()).then(d=>_ss(d)).catch(()=>{});},[_un]);'
              'if(!_s)return null;')
NEW_UC_DEF = ('function _UserCard({username:_un,onMessage:_om,record:_br,stats:_ps})'
              '{const[_s,_ss]=(0,_.useState)(_ps||null);'
              '(0,_.useEffect)(()=>{if(_ps||!_un)return;'
              'fetch(`${R}/user-stats?username=${encodeURIComponent(_un)}`)'
              '.then(r=>r.json()).then(d=>_ss(d)).catch(()=>{});},[_un]);'
              'if(!_s)return null;')
if OLD_UC_DEF in content:
    content = content.replace(OLD_UC_DEF, NEW_UC_DEF, 1)
    print('OK: _UserCard accepts stats prop')
else:
    errors.append('FAIL: _UserCard definition not found')

# ── B1. qr(): add _gpStats state ─────────────────────────────────────────────
OLD_GP_STATE = '[_gpBird,_setGpBird]=(0,_.useState)(null),[f,p]=(0,_.useState)(0)'
NEW_GP_STATE = '[_gpBird,_setGpBird]=(0,_.useState)(null),[_gpStats,_setGpStats]=(0,_.useState)(null),[f,p]=(0,_.useState)(0)'
if OLD_GP_STATE in content:
    content = content.replace(OLD_GP_STATE, NEW_GP_STATE, 1)
    print('OK: _gpStats state added to qr()')
else:
    errors.append('FAIL: _gpBird state anchor not found')

# ── B2. qr(): pill click handler — fetch stats first ─────────────────────────
OLD_GP_CLICK = ('if(ev.target.closest(`button`))return;'
                'ev.stopPropagation();'
                '_setGpBird(un);')
NEW_GP_CLICK = ('if(ev.target.closest(`button`))return;'
                'ev.stopPropagation();'
                'fetch(`${R}/user-stats?username=${encodeURIComponent(un)}`)'
                '.then(r=>r.json())'
                '.then(d=>{_setGpStats(d);_setGpBird(un);})'
                '.catch(()=>_setGpBird(un));')
if OLD_GP_CLICK in content:
    content = content.replace(OLD_GP_CLICK, NEW_GP_CLICK, 1)
    print('OK: global pill click fetches stats first')
else:
    errors.append('FAIL: global pill click handler not found')

# ── B3. qr(): pass stats to _UserCard in global overlay ──────────────────────
OLD_GP_UC = '(0,L.jsx)(_UserCard,{username:_gpBird})'
NEW_GP_UC = '(0,L.jsx)(_UserCard,{username:_gpBird,stats:_gpStats})'
if OLD_GP_UC in content:
    content = content.replace(OLD_GP_UC, NEW_GP_UC, 1)
    print('OK: stats passed to _UserCard in global overlay')
else:
    errors.append('FAIL: global overlay _UserCard not found')

# ── B4. qr(): clear _gpStats on close (outer div + tap-to-close button) ──────
# outer overlay div onClick
OLD_GP_CLOSE1 = ('onClick:()=>_setGpBird(null),'
                 'style:{position:`fixed`,inset:0,background:`rgba(0,0,0,0.6)`,zIndex:2000')
NEW_GP_CLOSE1 = ('onClick:()=>{_setGpBird(null);_setGpStats(null);},'
                 'style:{position:`fixed`,inset:0,background:`rgba(0,0,0,0.6)`,zIndex:2000')
if OLD_GP_CLOSE1 in content:
    content = content.replace(OLD_GP_CLOSE1, NEW_GP_CLOSE1, 1)
    print('OK: global overlay outer close clears stats')
else:
    errors.append('FAIL: global overlay outer close not found')

# tap-to-close button onClick
OLD_GP_CLOSE2 = ('onClick:()=>_setGpBird(null),'
                 'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,'
                 'fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`')
NEW_GP_CLOSE2 = ('onClick:()=>{_setGpBird(null);_setGpStats(null);},'
                 'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,'
                 'fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`')
if OLD_GP_CLOSE2 in content:
    content = content.replace(OLD_GP_CLOSE2, NEW_GP_CLOSE2, 1)
    print('OK: global overlay tap-to-close clears stats')
else:
    errors.append('FAIL: global tap-to-close not found')

# ── C1. Rr: add _birdStats state ──────────────────────────────────────────────
OLD_BIRD_STATE = '[_birdOpen,_setBirdOpen]=(0,_.useState)(!1),'
NEW_BIRD_STATE = '[_birdOpen,_setBirdOpen]=(0,_.useState)(!1),[_birdStats,_setBirdStats]=(0,_.useState)(null),'
if OLD_BIRD_STATE in content:
    content = content.replace(OLD_BIRD_STATE, NEW_BIRD_STATE, 1)
    print('OK: _birdStats state added to Rr')
else:
    errors.append('FAIL: _birdOpen state in Rr not found')

# ── C2. Rr: Bird button click — fetch stats first ─────────────────────────────
OLD_BIRD_CLICK = "onClick:()=>{y(!1);_setBirdOpen(!0)},children:`Bird`"
NEW_BIRD_CLICK = ("onClick:()=>{y(!1);"
                  "fetch(`${R}/user-stats?username=${encodeURIComponent(e.username)}`)"
                  ".then(r=>r.json())"
                  ".then(d=>{_setBirdStats(d);_setBirdOpen(!0);})"
                  ".catch(()=>_setBirdOpen(!0));}"
                  ",children:`Bird`")
if OLD_BIRD_CLICK in content:
    content = content.replace(OLD_BIRD_CLICK, NEW_BIRD_CLICK, 1)
    print('OK: Rr Bird button fetches stats first')
else:
    errors.append('FAIL: Rr Bird button onClick not found')

# ── C3. Rr: pass stats to _UserCard in comment overlay ───────────────────────
OLD_BIRD_UC = '(0,L.jsx)(_UserCard,{username:e.username,record:e})'
NEW_BIRD_UC = '(0,L.jsx)(_UserCard,{username:e.username,record:e,stats:_birdStats})'
if OLD_BIRD_UC in content:
    content = content.replace(OLD_BIRD_UC, NEW_BIRD_UC, 1)
    print('OK: stats passed to _UserCard in comment overlay')
else:
    errors.append('FAIL: comment overlay _UserCard not found')

# ── C4. Rr: clear _birdStats on close (outer div + tap-to-close button) ──────
OLD_BIRD_CLOSE1 = ('onClick:()=>_setBirdOpen(!1),'
                   'style:{position:`fixed`,inset:0,background:`rgba(0,0,0,0.6)`,zIndex:1000')
NEW_BIRD_CLOSE1 = ('onClick:()=>{_setBirdOpen(!1);_setBirdStats(null);},'
                   'style:{position:`fixed`,inset:0,background:`rgba(0,0,0,0.6)`,zIndex:1000')
if OLD_BIRD_CLOSE1 in content:
    content = content.replace(OLD_BIRD_CLOSE1, NEW_BIRD_CLOSE1, 1)
    print('OK: comment overlay outer close clears stats')
else:
    errors.append('FAIL: comment overlay outer close not found')

OLD_BIRD_CLOSE2 = ('onClick:()=>_setBirdOpen(!1),'
                   'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,'
                   'fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`')
NEW_BIRD_CLOSE2 = ('onClick:()=>{_setBirdOpen(!1);_setBirdStats(null);},'
                   'style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,'
                   'fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`')
if OLD_BIRD_CLOSE2 in content:
    content = content.replace(OLD_BIRD_CLOSE2, NEW_BIRD_CLOSE2, 1)
    print('OK: comment overlay tap-to-close clears stats')
else:
    errors.append('FAIL: comment tap-to-close not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
