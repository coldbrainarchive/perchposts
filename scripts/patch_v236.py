#!/usr/bin/env python3
"""Patch v235 -> v236: Flock cards — tap to reveal action buttons and IP."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v235.js'
dst = '_deploy/assets/index-DUcNPOLc-v236.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _expId state to Gr ─────────────────────────────────────────────────
OLD_STATE = '[he,ge]=(0,_.useState)(`active_desc`),_e=(0,_.useCallback)'
NEW_STATE = '[he,ge]=(0,_.useState)(`active_desc`),[_expId,_setExpId]=(0,_.useState)(null),_e=(0,_.useCallback)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _expId state added to Gr')
else:
    errors.append('FAIL: Gr state anchor not found')

# ── 2. Add onClick + cursor to member card outer div ─────────────────────────
OLD_CARD = (
    'style:{padding:`12px 16px`,borderBottom:r<t.length-1?`1px solid #2e303a`:`none`,background:p},'
    'children:['
)
NEW_CARD = (
    'style:{padding:`12px 16px`,borderBottom:r<t.length-1?`1px solid #2e303a`:`none`,background:p,'
    'cursor:`pointer`},onClick:()=>_setExpId(n.id===_expId?null:n.id),'
    'children:['
)
if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD, 1)
    print('OK: member card click handler added')
else:
    errors.append('FAIL: member card outer div not found')

# ── 3. Show IP only when expanded ─────────────────────────────────────────────
OLD_IP = (
    'n.user_metadata?.ip_hash?` \xb7 IP: ${n.user_metadata.ip_hash.slice(0,8)}…`:``'
)
NEW_IP = (
    'n.id===_expId&&n.user_metadata?.ip_hash?` \xb7 IP: ${n.user_metadata.ip_hash.slice(0,8)}…`:``'
)
if OLD_IP in content:
    content = content.replace(OLD_IP, NEW_IP, 1)
    print('OK: IP gated on expand')
else:
    errors.append('FAIL: IP display not found')

# ── 4. Show buttons only when expanded ───────────────────────────────────────
OLD_BTNS = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:4,flexWrap:`wrap`,marginTop:4},'
    'children:[!d&&(0,L.jsxs)(L.Fragment'
)
NEW_BTNS = (
    'n.id===_expId&&(0,L.jsxs)(`div`,{style:{display:`flex`,gap:4,flexWrap:`wrap`,marginTop:4},'
    'children:[!d&&(0,L.jsxs)(L.Fragment'
)
if OLD_BTNS in content:
    content = content.replace(OLD_BTNS, NEW_BTNS, 1)
    print('OK: buttons gated on expand')
else:
    errors.append('FAIL: button row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
