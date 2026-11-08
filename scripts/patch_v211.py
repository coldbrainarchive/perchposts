#!/usr/bin/env python3
"""Patch v210 -> v211: move pin/lock/bot chips to top-right corner of postcard."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v210.js'
dst = '_deploy/assets/index-DUcNPOLc-v211.js'

content = open(src, encoding='utf-8').read()
errors = []

CHIP_STYLE = (
    'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
    'height:20,width:20,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`'
)
BOT_CHIP_STYLE = (
    'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
    'height:20,width:20,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:13,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`'
)

# ── 1. Add position:relative to feed-post-card CSS ───────────────────────────
OLD_CSS = '.feed-post-card {\n        padding: 18px 20px 17px;\n      }'
NEW_CSS = '.feed-post-card {\n        padding: 18px 20px 17px;\n        position: relative;\n      }'
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: feed-post-card position:relative')
else:
    errors.append('FAIL: feed-post-card CSS not found')

# ── 2. Remove pin/lock/bot from board-group, add top-right container ──────────
OLD = (
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
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)?'
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:22,width:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:14,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`🤖`}):null'
    ']})})'
)
NEW = (
    # close the board-group and board-row
    ']})})'
    # absolutely positioned top-right cluster
    ',(e.pinned||e.locked||e.browser_id&&String(e.browser_id).startsWith(`bot-`))&&'
    '(0,L.jsxs)(`div`,{style:{position:`absolute`,top:14,right:16,'
    'display:`flex`,gap:4,alignItems:`center`},children:['
    'e.pinned&&(0,L.jsx)(`span`,{style:{' + CHIP_STYLE + '},children:`📌`}),'
    'e.locked&&(0,L.jsx)(`span`,{style:{' + CHIP_STYLE + '},children:`🔒`}),'
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)&&'
    '(0,L.jsx)(`span`,{style:{' + BOT_CHIP_STYLE + '},children:`🤖`})'
    ']})'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: pin/lock/bot moved to top-right corner')
else:
    errors.append('FAIL: chip pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
