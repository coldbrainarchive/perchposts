#!/usr/bin/env python3
"""Patch v509 -> v510:
- Rename "Archive" section to "Deleted"
- Add View button to deleted posts
- Add Delete All button to deleted section
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v509.js'
dst = '_deploy/assets/index-DUcNPOLc-v510.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Rename header "Archive" -> "Deleted" and add Delete All button ─────────
OLD_HDR = ('children:[`Archive `,(0,L.jsx)(`span`,{style:{color:`#64748b`,fontWeight:500,fontSize:13},'
           'children:d.length})]}),p&&(0,L.jsx)(`input`,{placeholder:`Search archive…`,'
           'value:h,onChange:e=>{e.stopPropagation(),g(e.target.value)},'
           'onClick:e=>e.stopPropagation(),'
           'style:{padding:`6px 12px`,borderRadius:10,border:`1px solid #3f4756`,'
           'background:`#0f1117`,color:`#f8fafc`,fontSize:13,width:180}}),'
           '(0,L.jsx)(`span`,{style:{color:`#64748b`,fontSize:13},children:p?`▲`:`▼`})')
NEW_HDR = ('children:[`Deleted `,(0,L.jsx)(`span`,{style:{color:`#64748b`,fontWeight:500,fontSize:13},'
           'children:d.length})]}),p&&d.length>0&&(0,L.jsx)(`button`,{'
           'onClick:async()=>{if(!confirm(`Permanently delete all ${d.length} deleted posts?`))return;'
           'await Promise.all(d.map(e=>zr({type:`permanent_delete_post`,post_id:e.id})));_e()},'
           'style:{padding:`4px 10px`,borderRadius:8,border:`none`,background:`#450a0a`,'
           'color:`#f87171`,fontWeight:600,fontSize:12,cursor:`pointer`},'
           'children:`Delete All`}),'
           'p&&(0,L.jsx)(`input`,{placeholder:`Search deleted…`,'
           'value:h,onChange:e=>{e.stopPropagation(),g(e.target.value)},'
           'onClick:e=>e.stopPropagation(),'
           'style:{padding:`6px 12px`,borderRadius:10,border:`1px solid #3f4756`,'
           'background:`#0f1117`,color:`#f8fafc`,fontSize:13,width:180}}),'
           '(0,L.jsx)(`span`,{style:{color:`#64748b`,fontSize:13},children:p?`▲`:`▼`})')
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: header renamed to Deleted, Delete All button added')
else:
    errors.append('FAIL: archive header not found')

# ── 2. Add View button to deleted posts (before Restore) ─────────────────────
OLD_BTNS = ('(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`restore_post`,post_id:e.id}),_e()},'
            'style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,'
            'color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Restore`}),'
            '(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete this post?`))return;'
            'await zr({type:`permanent_delete_post`,post_id:e.id});_e()},'
            'style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#450a0a`,'
            'color:`#f87171`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Delete`})')
NEW_BTNS = ('(0,L.jsx)(`a`,{href:`/post/${e.id}`,target:`_blank`,'
            'style:{padding:`6px 12px`,borderRadius:8,border:`none`,'
            'background:`#1e3a5f`,color:`#60a5fa`,fontWeight:600,fontSize:12,'
            'cursor:`pointer`,textDecoration:`none`,display:`inline-block`},'
            'children:`View`}),'
            '(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`restore_post`,post_id:e.id}),_e()},'
            'style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,'
            'color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Restore`}),'
            '(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete this post?`))return;'
            'await zr({type:`permanent_delete_post`,post_id:e.id});_e()},'
            'style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#450a0a`,'
            'color:`#f87171`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Delete`})')
if OLD_BTNS in content:
    content = content.replace(OLD_BTNS, NEW_BTNS, 1)
    print('OK: View button added to deleted posts')
else:
    errors.append('FAIL: deleted post buttons not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
