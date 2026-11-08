#!/usr/bin/env python3
"""Patch v217 -> v218: post view matches postcard — bot has no username, pin/lock/bot go top-right."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v217.js'
dst = '_deploy/assets/index-DUcNPOLc-v218.js'

content = open(src, encoding='utf-8').read()
errors = []

CHIP = (
    'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
    'height:20,width:20,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`'
)
TOP_RIGHT = (
    '(c.pinned||c.locked||c.browser_id&&String(c.browser_id).startsWith(`bot-`))&&'
    '(0,L.jsxs)(`div`,{style:{position:`absolute`,top:14,right:16,'
    'display:`flex`,gap:4,alignItems:`center`},children:['
    'c.pinned&&(0,L.jsx)(`span`,{style:{' + CHIP + '},children:`📌`}),'
    'c.locked&&(0,L.jsx)(`span`,{style:{' + CHIP + '},children:`🔒`}),'
    'c.browser_id&&String(c.browser_id).startsWith(`bot-`)&&'
    '(0,L.jsx)(`span`,{style:{' + CHIP.replace('fontSize:11','fontSize:13') + '},children:`🤖`})'
    ']})'
)

OLD = (
    'feed-post-board-group`,style:{flexWrap:`wrap`,gap:5},'
    'children:[(0,L.jsx)(Xn,{record:c,name:le,color:Hn(c.browser_id,c.username)}),'
    'ce&&(()=>{let e=nr.find(e=>e.name===ce)?.slug;'
    'return e?(0,L.jsx)(I,{to:`/board/${e}`,style:{textDecoration:`none`,'
    'display:`inline-flex`,alignItems:`center`},'
    'children:(0,L.jsx)(Ar,{boardName:ce,small:!0})}):'
    '(0,L.jsx)(Ar,{boardName:ce,small:!0})})(),'
    '(c.country||c.continent)&&(0,L.jsx)(kr,{country:c.country,continent:c.continent,small:!0}),'
    'c.pinned&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`📌`}),'
    'c.locked&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`🔒`})'
    ']})})'
)
NEW = (
    'feed-post-board-group`,style:{flexWrap:`wrap`,gap:5},'
    'children:['
    # no user pill for bots
    '!c.browser_id||!String(c.browser_id).startsWith(`bot-`)?'
    '(0,L.jsx)(Xn,{record:c,name:le,color:Hn(c.browser_id,c.username)}):null,'
    'ce&&(()=>{let e=nr.find(e=>e.name===ce)?.slug;'
    'return e?(0,L.jsx)(I,{to:`/board/${e}`,style:{textDecoration:`none`,'
    'display:`inline-flex`,alignItems:`center`},'
    'children:(0,L.jsx)(Ar,{boardName:ce,small:!0})}):'
    '(0,L.jsx)(Ar,{boardName:ce,small:!0})})(),'
    '(c.country||c.continent)&&(0,L.jsx)(kr,{country:c.country,continent:c.continent,small:!0})'
    # close board-group, board-row
    ']})})'
    # top-right cluster
    ',' + TOP_RIGHT
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: post view board-group updated')
else:
    errors.append('FAIL: post view board-group not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
