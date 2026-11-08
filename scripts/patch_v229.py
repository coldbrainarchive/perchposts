#!/usr/bin/env python3
"""Patch v228 -> v229: mod panel archive — add content preview + permanent delete button (remove broken View link)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v228.js'
dst = '_deploy/assets/index-DUcNPOLc-v229.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the archive card buttons area:
# - Remove broken View <Link> (deleted posts return 404)
# - Add content preview inline (e.content is returned by the mod-panel fetch)
# - Keep Restore button
# - Add permanent Delete button
OLD = (
    'children:Un(e.created_at)})]})]}),(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,flexShrink:0},'
    'children:[(0,L.jsx)(I,{to:`/post/${e.id}`,style:{padding:`6px 12px`,borderRadius:8,'
    'border:`1px solid #374151`,background:`#1f2937`,color:`#f8fafc`,fontWeight:600,fontSize:12,'
    'textDecoration:`none`},children:`View`}),(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`restore_post`,'
    'post_id:e.id}),_e()},style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,'
    'color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Restore`})]})'
)
NEW = (
    'children:Un(e.created_at)})]}),'
    'e.content&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginTop:6,'
    'overflow:`hidden`,display:`-webkit-box`,WebkitLineClamp:2,WebkitBoxOrient:`vertical`},'
    'children:e.content})]}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,flexShrink:0},'
    'children:[(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`restore_post`,'
    'post_id:e.id}),_e()},style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,'
    'color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Restore`}),'
    '(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete this post?`))return;'
    'await zr({type:`permanent_delete_post`,post_id:e.id});_e()},style:{padding:`6px 12px`,'
    'borderRadius:8,border:`none`,background:`#450a0a`,color:`#f87171`,fontWeight:600,fontSize:12,'
    'cursor:`pointer`},children:`Delete`})]})'
)

count = content.count(OLD)
if count > 0:
    content = content.replace(OLD, NEW)
    print(f'OK: archive card updated — content preview + delete button ({count} occurrence(s))')
else:
    errors.append('FAIL: archive card button area not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
