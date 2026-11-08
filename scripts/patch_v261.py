#!/usr/bin/env python3
"""Patch v260 -> v261: admin tag in DM header matches user card; reply btn inside picker only."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v260.js'
dst = '_deploy/assets/index-DUcNPOLc-v261.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Thread header: pass is_admin/is_mod from _dmConvs for correct Xn tag ──
OLD_HDR = '(0,L.jsx)(Xn,{record:{username:_dmThread},name:_dmThread,color:Hn(null,_dmThread)})'
NEW_HDR = (
    '(()=>{const _tc=_dmConvs.find(c=>c.contact===_dmThread)||{};'
    'return(0,L.jsx)(Xn,{record:{username:_dmThread,'
    'is_admin:!!_tc.is_admin,is_mod:!!_tc.is_mod},'
    'name:_dmThread,'
    'color:_tc.is_admin?`#ffffff`:Hn(null,_dmThread)})})()'
)
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: thread header Xn uses is_admin/is_mod from _dmConvs')
else:
    errors.append('FAIL: thread header Xn not found')

# ── 2. Move reply button inside picker row (only shows when picker is open) ───
# Currently: bubble + reply_btn are always together, then picker below
# New: bubble alone, picker row includes reply btn at the end

# Remove the always-visible reply button from the bubble row
OLD_REPLY_ALWAYS = (
    '(0,L.jsx)(`button`,{onClick:()=>{_setDmReplyTo(_msg);_setDmPickerId(null);},'
    'style:{background:`none`,border:`none`,color:`#475569`,fontSize:13,'
    'cursor:`pointer`,padding:`2px 4px`,opacity:0.6,flexShrink:0},'
    'children:`↩`})]})'
)
NEW_REPLY_ALWAYS = ']})'   # just close the bubble row, no reply btn
if OLD_REPLY_ALWAYS in content:
    content = content.replace(OLD_REPLY_ALWAYS, NEW_REPLY_ALWAYS, 1)
    print('OK: always-visible reply button removed from bubble row')
else:
    errors.append('FAIL: always-visible reply button not found')

# Add reply button at end of emoji picker row
OLD_PICKER_END = (
    'style:{background:`none`,border:`none`,fontSize:14,cursor:`pointer`,padding:`1px 3px`,'
    'borderRadius:6,opacity:0.6},children:`🔥`})]}),'
)
NEW_PICKER_END = (
    'style:{background:`none`,border:`none`,fontSize:14,cursor:`pointer`,padding:`1px 3px`,'
    'borderRadius:6,opacity:0.6},children:`🔥`}),'
    # Reply button at end of picker row
    '(0,L.jsx)(`button`,{onClick:()=>{_setDmReplyTo(_msg);_setDmPickerId(null);},'
    'style:{background:`none`,border:`none`,color:`#94a3b8`,fontSize:13,'
    'cursor:`pointer`,padding:`1px 4px`,borderRadius:6,opacity:0.8,flexShrink:0},'
    'children:`↩`})]}),'
)
if OLD_PICKER_END in content:
    content = content.replace(OLD_PICKER_END, NEW_PICKER_END, 1)
    print('OK: reply button moved inside picker row')
else:
    errors.append('FAIL: picker end not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
