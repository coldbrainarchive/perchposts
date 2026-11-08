#!/usr/bin/env python3
"""Patch v205 -> v206: bot posts show 🤖 chip instead of username pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v205.js'
dst = '_deploy/assets/index-DUcNPOLc-v206.js'

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
    '(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,'
    'color:Hn(e.browser_id,e.username),'
    'onClick:e.username?t=>m(`user`,e.username,t):void 0})'
)
NEW = (
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)'
    '?' + BOT_CHIP + ''
    ':(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,'
    'color:Hn(e.browser_id,e.username),'
    'onClick:e.username?t=>m(`user`,e.username,t):void 0})'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: bot posts show 🤖 chip instead of username pill')
else:
    errors.append('FAIL: Xn author pill in postcard not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
