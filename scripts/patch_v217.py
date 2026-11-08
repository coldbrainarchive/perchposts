#!/usr/bin/env python3
"""Patch v216 -> v217: bot filter — chip in search bar; clicking 🤖 on postcard filters to bots only."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v216.js'
dst = '_deploy/assets/index-DUcNPOLc-v217.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Vr feed: read ?bot= param and filter posts ─────────────────────────────
OLD_VR_PARAM = 'qT=l.get(`time`)||``,'
NEW_VR_PARAM = 'qT=l.get(`time`)||``,_bot=l.get(`bot`)||``,'
if OLD_VR_PARAM in content:
    content = content.replace(OLD_VR_PARAM, NEW_VR_PARAM, 1)
    print('OK: _bot param added to Vr')
else:
    errors.append('FAIL: qT param line in Vr not found')

# ── 2. Vr feed: include _bot in _bl source selection & add filter ─────────────
OLD_BL = (
    'let y=u===`activity`,_bl=m&&SR!==null?SR:qT&&TR!==null?TR:'
    '(u||d||f||p)&&!y&&TagR!==null?TagR:e,'
    'b=_bl.filter(e=>u?y?fr.includes(e.username)?'
    '(n[e.id]||0)>0||(i[e.id]?.voteCount??0)>0:!0:cr(e)===(sr(u)?.name||u):!0)'
    '.filter(e=>!d||e.continent===d)'
    '.filter(e=>!f||e.country===f)'
    '.filter(e=>!p||(e.username||``).toLowerCase()===p)'
)
NEW_BL = (
    'let y=u===`activity`,_bl=m&&SR!==null?SR:qT&&TR!==null?TR:'
    '(u||d||f||p||_bot)&&!y&&TagR!==null?TagR:e,'
    'b=_bl.filter(e=>u?y?fr.includes(e.username)?'
    '(n[e.id]||0)>0||(i[e.id]?.voteCount??0)>0:!0:cr(e)===(sr(u)?.name||u):!0)'
    '.filter(e=>!_bot||!!(e.browser_id&&String(e.browser_id).startsWith(`bot-`)))'
    '.filter(e=>!d||e.continent===d)'
    '.filter(e=>!f||e.country===f)'
    '.filter(e=>!p||(e.username||``).toLowerCase()===p)'
)
if OLD_BL in content:
    content = content.replace(OLD_BL, NEW_BL, 1)
    print('OK: bot filter added to Vr')
else:
    errors.append('FAIL: _bl filter chain not found')

# ── 3. Lr search bar: read _botF, add clear fn, add chip, update M ────────────
OLD_LR_VARS = 'let j=nr.find(e=>e.slug===d),M=d||f||p||m||q2;'
NEW_LR_VARS = (
    'let _botF=e.get(`bot`)||``,'
    '_clearBot=()=>{let n=new URLSearchParams(e);n.delete(`bot`);t(n)};'
    'let j=nr.find(e=>e.slug===d),M=d||f||p||m||q2||_botF;'
)
if OLD_LR_VARS in content:
    content = content.replace(OLD_LR_VARS, NEW_LR_VARS, 1)
    print('OK: _botF var and clear fn added to Lr')
else:
    errors.append('FAIL: Lr M variable line not found')

# Add bot chip after q2 chip in search bar, before the input
OLD_CHIP_END = (
    'q2&&(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
    'style:{background:`rgba(192,132,252,0.15)`,borderColor:`#c084fc55`,color:`#c084fc`},'
    'onClick:e=>{e.stopPropagation(),ae()},'
    'children:[(0,L.jsx)(`span`,{children:`🕐 `+(q2&&q2.startsWith(`ago_`)?q2.slice(4)+`h ago`:q2)})]})'
    ',(0,L.jsx)(`input`,'
)
NEW_CHIP_END = (
    'q2&&(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
    'style:{background:`rgba(192,132,252,0.15)`,borderColor:`#c084fc55`,color:`#c084fc`},'
    'onClick:e=>{e.stopPropagation(),ae()},'
    'children:[(0,L.jsx)(`span`,{children:`🕐 `+(q2&&q2.startsWith(`ago_`)?q2.slice(4)+`h ago`:q2)})]})'
    ',_botF&&(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
    'style:{background:`rgba(192,132,252,0.15)`,borderColor:`#c084fc55`,color:`#c084fc`},'
    'onClick:e=>{e.stopPropagation(),_clearBot()},'
    'children:[(0,L.jsx)(`span`,{children:`🤖 Bots`})]})'
    ',(0,L.jsx)(`input`,'
)
if OLD_CHIP_END in content:
    content = content.replace(OLD_CHIP_END, NEW_CHIP_END, 1)
    print('OK: bot chip added to Lr search bar')
else:
    errors.append('FAIL: q2 chip end / input not found')

# ── 4. Postcard: make 🤖 top-right chip a clickable button ───────────────────
OLD_BOT_CHIP = (
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)&&'
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:20,width:20,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:13,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`},'
    'children:`🤖`})'
)
NEW_BOT_CHIP = (
    'e.browser_id&&String(e.browser_id).startsWith(`bot-`)&&'
    '(0,L.jsx)(`button`,{type:`button`,onClick:_e=>m(`bot`,`1`,_e),'
    'style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,height:20,width:20,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,'
    'fontSize:13,flexShrink:0,lineHeight:1,overflow:`hidden`,'
    'boxSizing:`border-box`,cursor:`pointer`},'
    'children:`🤖`})'
)
if OLD_BOT_CHIP in content:
    content = content.replace(OLD_BOT_CHIP, NEW_BOT_CHIP, 1)
    print('OK: 🤖 chip is now a clickable button')
else:
    errors.append('FAIL: top-right bot chip not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
