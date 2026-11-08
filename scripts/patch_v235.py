#!/usr/bin/env python3
"""Patch v234 -> v235: Flock panel — much smaller action buttons, show IP hash."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v234.js'
dst = '_deploy/assets/index-DUcNPOLc-v235.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add IP to meta line (after rank/worm line) ────────────────────────────
OLD_META_END = (
    'return _wr?` \xb7 ${_wr.e} ${_wr.n} \xb7 \U0001fab1 ${_wc}`:``;})()]})'
)
NEW_META_END = (
    'return _wr?` \xb7 ${_wr.e} ${_wr.n} \xb7 \U0001fab1 ${_wc}`:``;})(),'
    'n.user_metadata?.ip_hash?` \xb7 IP: ${n.user_metadata.ip_hash.slice(0,8)}…`:``]})'
)
if OLD_META_END in content:
    content = content.replace(OLD_META_END, NEW_META_END, 1)
    print('OK: IP hash added to meta line')
else:
    errors.append('FAIL: meta line end not found')

# ── 2. Cage button — tiny ─────────────────────────────────────────────────────
OLD_CAGE = (
    'onClick:()=>Ce(o),style:{flex:1,padding:`5px 8px`,borderRadius:10,border:`none`,'
    'background:c?`#78350f`:`#451a03`,color:c?`#fde68a`:`#fbbf24`,fontWeight:700,cursor:`pointer`,fontSize:11}'
)
NEW_CAGE = (
    'onClick:()=>Ce(o),style:{padding:`2px 8px`,borderRadius:6,border:`none`,'
    'background:c?`#78350f`:`#451a03`,color:c?`#fde68a`:`#fbbf24`,fontWeight:600,cursor:`pointer`,fontSize:10}'
)
if OLD_CAGE in content:
    content = content.replace(OLD_CAGE, NEW_CAGE, 1)
    print('OK: cage button shrunk')
else:
    errors.append('FAIL: cage button not found')

# ── 3. Ban button — tiny ──────────────────────────────────────────────────────
OLD_BAN = (
    'onClick:()=>xe(o),style:{flex:1,padding:`5px 8px`,borderRadius:10,border:`none`,'
    'background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:700,cursor:`pointer`,fontSize:11}'
)
NEW_BAN = (
    'onClick:()=>xe(o),style:{padding:`2px 8px`,borderRadius:6,border:`none`,'
    'background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:600,cursor:`pointer`,fontSize:10}'
)
if OLD_BAN in content:
    content = content.replace(OLD_BAN, NEW_BAN, 1)
    print('OK: ban button shrunk')
else:
    errors.append('FAIL: ban button not found')

# ── 4. Mod/Demote button — tiny ───────────────────────────────────────────────
OLD_MOD = (
    'style:{flex:1,padding:`7px 4px`,borderRadius:10,border:`none`,'
    'background:f?`#1f2937`:`#c084fc`,color:f?`#f8fafc`:`#14081d`,'
    'fontWeight:700,fontSize:12,cursor:`pointer`}'
)
NEW_MOD = (
    'style:{padding:`2px 8px`,borderRadius:6,border:`none`,'
    'background:f?`#1f2937`:`#c084fc`,color:f?`#f8fafc`:`#14081d`,'
    'fontWeight:600,fontSize:10,cursor:`pointer`}'
)
if OLD_MOD in content:
    content = content.replace(OLD_MOD, NEW_MOD, 1)
    print('OK: mod button shrunk')
else:
    errors.append('FAIL: mod button not found')

# ── 5. Admin button — tiny ────────────────────────────────────────────────────
OLD_ADMIN = (
    'style:{flex:1,padding:`7px 4px`,borderRadius:10,border:`none`,'
    'background:`#fb923c`,color:`#14081d`,fontWeight:700,fontSize:12,cursor:`pointer`}'
)
NEW_ADMIN = (
    'style:{padding:`2px 8px`,borderRadius:6,border:`none`,'
    'background:`#fb923c`,color:`#14081d`,fontWeight:600,fontSize:10,cursor:`pointer`}'
)
if OLD_ADMIN in content:
    content = content.replace(OLD_ADMIN, NEW_ADMIN, 1)
    print('OK: admin button shrunk')
else:
    errors.append('FAIL: admin button not found')

# ── 6. Delete button — tiny ───────────────────────────────────────────────────
OLD_DEL = (
    'style:{flex:1,padding:`7px 4px`,borderRadius:10,'
    'border:`1px solid #374151`,background:`transparent`,'
    'color:`#f87171`,fontWeight:700,fontSize:12,cursor'
)
NEW_DEL = (
    'style:{padding:`2px 8px`,borderRadius:6,'
    'border:`1px solid #374151`,background:`transparent`,'
    'color:`#f87171`,fontWeight:600,fontSize:10,cursor'
)
if OLD_DEL in content:
    content = content.replace(OLD_DEL, NEW_DEL, 1)
    print('OK: delete button shrunk')
else:
    errors.append('FAIL: delete button not found')

# ── 7. Button row: remove flexWrap and reduce gap ────────────────────────────
OLD_BTN_ROW = 'display:`flex`,gap:6,flexWrap:`wrap`},children:[!d&&(0,L.jsxs)(L.Fragment'
NEW_BTN_ROW = 'display:`flex`,gap:4,flexWrap:`wrap`,marginTop:4},children:[!d&&(0,L.jsxs)(L.Fragment'
if OLD_BTN_ROW in content:
    content = content.replace(OLD_BTN_ROW, NEW_BTN_ROW, 1)
    print('OK: button row gap reduced')
else:
    errors.append('FAIL: button row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
