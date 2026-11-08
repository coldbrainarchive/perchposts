#!/usr/bin/env python3
"""Patch v508 -> v509:
- Add Archive button for mods on post page
- Add Archived posts section in admin panel (separate from Deleted)
- Wire up archivedPosts state and rendering
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v508.js'
dst = '_deploy/assets/index-DUcNPOLc-v509.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add Archive button next to Delete on post page (mod only) ──────────────
OLD_DEL_BTN = ('N&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
               'onClick:async()=>{if(!confirm(`Are you sure?`))return;'
               'await zr({type:`delete_post`,post_id:c.id});o(`/`)},children:`Delete`})')
NEW_DEL_BTN = ('N&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
               'onClick:async()=>{if(!confirm(`Are you sure?`))return;'
               'await zr({type:`delete_post`,post_id:c.id});o(`/`)},children:`Delete`}),'
               'N&&!c.archived&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
               'onClick:async()=>{if(!confirm(`Archive this post? It will be hidden from the feed but viewable in the admin panel.`))return;'
               'await zr({type:`archive_post`,post_id:c.id});o(`/`)},children:`Archive`}),'
               'N&&c.archived&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
               'onClick:async()=>{await zr({type:`unarchive_post`,post_id:c.id}),P()},children:`Unarchive`})')
if OLD_DEL_BTN in content:
    content = content.replace(OLD_DEL_BTN, NEW_DEL_BTN, 1)
    print('OK: Archive/Unarchive button added to post page')
else:
    errors.append('FAIL: mod Delete button on post page not found')

# ── 2. Add archivedPosts state variables after deletedPosts state ─────────────
OLD_STATE = '[d,f]=(0,_.useState)([]),[p,m]=(0,_.useState)(!1),[h,g]=(0,_.useState)(``)'
NEW_STATE = '[d,f]=(0,_.useState)([]),[p,m]=(0,_.useState)(!1),[h,g]=(0,_.useState)(``),\
[_archPosts,_setArchPosts]=(0,_.useState)([]),[_archOpen,_setArchOpen]=(0,_.useState)(!1),[_archSrch,_setArchSrch]=(0,_.useState)(``)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: archivedPosts state added')
else:
    errors.append('FAIL: admin state declarations not found')

# ── 3. Wire archivedPosts data load ──────────────────────────────────────────
OLD_LOAD = 'f(l.deletedPosts||[])'
NEW_LOAD = 'f(l.deletedPosts||[]),_setArchPosts(l.archivedPosts||[])'
if OLD_LOAD in content:
    content = content.replace(OLD_LOAD, NEW_LOAD, 1)
    print('OK: archivedPosts data load wired')
else:
    errors.append('FAIL: deletedPosts load not found')

# ── 4. Add Archived section after the existing Deleted/Archive section ─────────
# Find the end of the existing archive (deleted posts) section to insert after it
# The section ends after the map() closes with }),} and before the next section
OLD_ARCH_END = ('children:`Restore`}),(0,L.jsx)(`button`,{onClick:async()=>'
                '{if(!confirm(`Permanently delete this post?`))return;'
                'await zr({type:`permanent_delete_post`,post_id:e.id});_e()},'
                'style:{padding:`6px 12px`,borderRadius:8,border:`none`,'
                'background:`#450a0a`,color:`#f87171`,fontWeight:600,fontSize:12,'
                'cursor:`pointer`},children:`Delete`})]})]},e.id)})')
NEW_ARCH_END = ('children:`Restore`}),(0,L.jsx)(`button`,{onClick:async()=>'
                '{if(!confirm(`Permanently delete this post?`))return;'
                'await zr({type:`permanent_delete_post`,post_id:e.id});_e()},'
                'style:{padding:`6px 12px`,borderRadius:8,border:`none`,'
                'background:`#450a0a`,color:`#f87171`,fontWeight:600,fontSize:12,'
                'cursor:`pointer`},children:`Delete`})]})]},e.id)})'
                # Archived section
                ',(0,L.jsxs)(`div`,{style:{borderTop:`1px solid #2e303a`,marginTop:8},'
                'children:['
                '(0,L.jsxs)(`div`,{style:{padding:`16px 20px`,borderBottom:_archOpen?`1px solid #2e303a`:`none`,'
                'display:`flex`,alignItems:`center`,gap:10,cursor:`pointer`},'
                'onClick:()=>_setArchOpen(e=>!e),'
                'children:['
                '(0,L.jsxs)(`h3`,{style:{margin:0,color:`#f8fafc`,fontSize:16,fontWeight:700,flex:1},'
                'children:[`Archived `,(0,L.jsx)(`span`,{style:{color:`#64748b`,fontWeight:500,fontSize:13},'
                'children:_archPosts.length})]}),'
                '_archOpen&&(0,L.jsx)(`input`,{placeholder:`Search archived…`,value:_archSrch,'
                'onChange:e=>{e.stopPropagation(),_setArchSrch(e.target.value)},'
                'onClick:e=>e.stopPropagation(),'
                'style:{padding:`6px 12px`,borderRadius:10,border:`1px solid #3f4756`,'
                'background:`#0f1117`,color:`#f8fafc`,fontSize:13,width:180}}),'
                '(0,L.jsx)(`span`,{style:{color:`#64748b`,fontSize:13},children:_archOpen?`▲`:`▼`})'
                ']}),'
                '_archOpen&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,'
                'maxHeight:520,overflowY:`auto`},children:['
                '_archPosts.length===0&&(0,L.jsx)(`div`,{style:{padding:`32px 20px`,color:`#64748b`,'
                'fontSize:14,textAlign:`center`},children:`No archived posts`}),'
                '_archPosts.filter(e=>!_archSrch.trim()||'
                'e.title?.toLowerCase().includes(_archSrch.toLowerCase())||'
                '(e.username||``).toLowerCase().includes(_archSrch.toLowerCase()))'
                '.map((e,t,n)=>{'
                'let r=cr(e),i=nr.find(e=>e.name===r);'
                'return(0,L.jsxs)(`div`,{style:{padding:`12px 16px`,'
                'borderBottom:t<n.length-1?`1px solid #2e303a`:`none`,'
                'display:`flex`,alignItems:`center`,gap:12},'
                'children:['
                '(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0},children:['
                '(0,L.jsx)(`div`,{style:{color:`#f8fafc`,fontWeight:600,fontSize:14,'
                'marginBottom:3,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},'
                'children:e.title||`—`}),'
                '(0,L.jsxs)(`div`,{style:{color:`#64748b`,fontSize:11,display:`flex`,'
                'alignItems:`center`,gap:6,flexWrap:`wrap`},'
                'children:[i&&(0,L.jsxs)(`span`,{style:{color:`#94a3b8`},'
                'children:[i.icon,` `,i.name]}),i&&(0,L.jsx)(`span`,{children:`·`}),'
                '(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,'
                'color:Hn(e.browser_id,e.username)}),'
                '(0,L.jsx)(`span`,{children:`·`}),'
                '(0,L.jsx)(`span`,{children:Un(e.created_at)})]}),'
                'e.content&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginTop:6,'
                'overflow:`hidden`,display:`-webkit-box`,WebkitLineClamp:2,'
                'WebkitBoxOrient:`vertical`},children:e.content})'
                ']})'
                ',(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,flexShrink:0},children:['
                '(0,L.jsx)(`a`,{href:`/post/${e.id}`,target:`_blank`,'
                'style:{padding:`6px 12px`,borderRadius:8,border:`none`,'
                'background:`#1e3a5f`,color:`#60a5fa`,fontWeight:600,fontSize:12,'
                'cursor:`pointer`,textDecoration:`none`,display:`inline-block`},'
                'children:`View`}),'
                '(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`unarchive_post`,post_id:e.id}),_e()},'
                'style:{padding:`6px 12px`,borderRadius:8,border:`none`,'
                'background:`#14532d`,color:`#4ade80`,fontWeight:600,fontSize:12,'
                'cursor:`pointer`},children:`Restore`}),'
                '(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete this post?`))return;'
                'await zr({type:`permanent_delete_post`,post_id:e.id}),_e()},'
                'style:{padding:`6px 12px`,borderRadius:8,border:`none`,'
                'background:`#450a0a`,color:`#f87171`,fontWeight:600,fontSize:12,'
                'cursor:`pointer`},children:`Delete`})'
                ']})]},e.id)})'
                ']})'
                ']})')
if OLD_ARCH_END in content:
    content = content.replace(OLD_ARCH_END, NEW_ARCH_END, 1)
    print('OK: Archived section added to admin panel')
else:
    errors.append('FAIL: end of deleted posts section not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
