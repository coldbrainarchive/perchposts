#!/usr/bin/env python3
"""Patch v233 -> v234: Flock panel cleanup — remove browser_id clutter, add worm count + rank."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v233.js'
dst = '_deploy/assets/index-DUcNPOLc-v234.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace browser_id in meta line with worm count + rank ────────────────
# Old: "Joined [date] · [browser_id] · active [time]"
# New: "Joined [date] · active [time] · 🪱 N · 🦅 RankName"
OLD_META = (
    '(0,L.jsxs)(`div`,{style:{color:`#475569`,fontSize:11,marginTop:1},'
    'children:[`Joined `,Un(n.created_at),a?` · ${a}`:``,'
    '(()=>{if(!n.last_active)return``;let d=Math.round((Date.now()-new Date(n.last_active))/6e4);'
    'return d<2?` · active just now`:d<60?` · active ${d}m ago`:'
    'd<1440?` · active ${Math.round(d/60)}h ago`:` · active ${Math.round(d/1440)}d ago`})()]})'
)
NEW_META = (
    '(0,L.jsxs)(`div`,{style:{color:`#475569`,fontSize:11,marginTop:1},'
    'children:[`Joined `,Un(n.created_at),'
    '(()=>{if(!n.last_active)return``;let d=Math.round((Date.now()-new Date(n.last_active))/6e4);'
    'return d<2?` · active just now`:d<60?` · active ${d}m ago`:'
    'd<1440?` · active ${Math.round(d/60)}h ago`:` · active ${Math.round(d/1440)}d ago`})(),'
    '(()=>{let _wc=n.worm_count||0,_wr=_RANKS.find(r=>_wc>=r.min&&_wc<=r.max);'
    'return _wr?` \xb7 ${_wr.e} ${_wr.n} \xb7 \U0001fab1 ${_wc}`:``;})()]})'
)
count = content.count(OLD_META)
if count > 0:
    content = content.replace(OLD_META, NEW_META)
    print(f'OK: meta line updated with worm count + rank ({count} occurrence(s))')
else:
    errors.append('FAIL: member meta line not found')

# ── 2. Make action buttons more compact (reduce vertical padding) ─────────────
# Cage/Uncage button: padding 7px 4px -> 5px 8px
OLD_BTN_CAGE = (
    'onClick:()=>Ce(o),style:{flex:1,padding:`7px 4px`,borderRadius:10,border:`none`,'
    'background:c?`#78350f`:`#451a03`,color:c?`#fde68a`:`#fbbf24`,fontWeight:700,cursor:`pointer`,fontSize:12}'
)
NEW_BTN_CAGE = (
    'onClick:()=>Ce(o),style:{flex:1,padding:`5px 8px`,borderRadius:10,border:`none`,'
    'background:c?`#78350f`:`#451a03`,color:c?`#fde68a`:`#fbbf24`,fontWeight:700,cursor:`pointer`,fontSize:11}'
)
if OLD_BTN_CAGE in content:
    content = content.replace(OLD_BTN_CAGE, NEW_BTN_CAGE, 1)
    print('OK: cage button compacted')
else:
    errors.append('FAIL: cage button not found')

# Ban button
OLD_BTN_BAN = (
    'onClick:()=>xe(o),style:{flex:1,padding:`7px 4px`,borderRadius:10,border:`none`,'
    'background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:700,cursor:`pointer`,fontSize:12}'
)
NEW_BTN_BAN = (
    'onClick:()=>xe(o),style:{flex:1,padding:`5px 8px`,borderRadius:10,border:`none`,'
    'background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:700,cursor:`pointer`,fontSize:11}'
)
if OLD_BTN_BAN in content:
    content = content.replace(OLD_BTN_BAN, NEW_BTN_BAN, 1)
    print('OK: ban button compacted')
else:
    errors.append('FAIL: ban button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
