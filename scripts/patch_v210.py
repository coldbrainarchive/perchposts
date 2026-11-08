#!/usr/bin/env python3
"""Patch v209 -> v210: move 🤖 chip to end of tag row (after pin/lock)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v209.js'
dst = '_deploy/assets/index-DUcNPOLc-v210.js'

content = open(src, encoding='utf-8').read()
errors = []

BOT_CHIP = (
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:14,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`🤖`})'
)

OLD = (
    # bot chip OR user pill at the start
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)?'
    + BOT_CHIP +
    ':(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,'
    'color:Hn(e.browser_id,e.username),'
    'onClick:e.username?t=>m(`user`,e.username,t):void 0}),'
    # board, country, pin, lock
    'd&&(0,L.jsx)(`button`,{type:`button`,onClick:e=>g?m(`board`,g,e):e.stopPropagation(),'
    'style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},'
    'children:(0,L.jsx)(Ar,{boardName:d,small:!0})}),'
    '(e.country||e.continent)&&(0,L.jsx)(`span`,{style:{cursor:`pointer`,'
    'display:`inline-flex`,alignItems:`center`},'
    'onClick:t=>e.country?m(`country`,e.country,t):m(`continent`,e.continent,t),'
    'children:(0,L.jsx)(kr,{country:e.country,continent:e.continent,small:!0})}),'
    'e.pinned&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`📌`}),'
    'e.locked&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`🔒`})'
)
NEW = (
    # user pill only (no bot check)
    '!e.browser_id||!String(e.browser_id).startsWith(`bot-`)?'
    '(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,'
    'color:Hn(e.browser_id,e.username),'
    'onClick:e.username?t=>m(`user`,e.username,t):void 0}):null,'
    # board, country, pin, lock (unchanged)
    'd&&(0,L.jsx)(`button`,{type:`button`,onClick:e=>g?m(`board`,g,e):e.stopPropagation(),'
    'style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},'
    'children:(0,L.jsx)(Ar,{boardName:d,small:!0})}),'
    '(e.country||e.continent)&&(0,L.jsx)(`span`,{style:{cursor:`pointer`,'
    'display:`inline-flex`,alignItems:`center`},'
    'onClick:t=>e.country?m(`country`,e.country,t):m(`continent`,e.continent,t),'
    'children:(0,L.jsx)(kr,{country:e.country,continent:e.continent,small:!0})}),'
    'e.pinned&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`📌`}),'
    'e.locked&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`🔒`}),'
    # bot chip at the end
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)?'
    + BOT_CHIP + ':null'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: 🤖 chip moved to end of tag row')
else:
    errors.append('FAIL: tag row pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
