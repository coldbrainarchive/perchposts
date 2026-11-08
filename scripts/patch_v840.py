#!/usr/bin/env python3
"""Patch v839 -> v840: archiving freezes a post, and the Mod Panel gets tabs.
Archived posts stay on the site with a badge and take no new chirps, wings or reactions. Hide from members
is a toggle in the Archived tab. Locked and archived posts can't be deleted by their author.
The Mod Panel splits into Flock, Archived, Deleted and Bot, with a title, preview and picture for each post.
Archived used to sit inside the Deleted card, so it only showed when Deleted was open.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v839.js'
dst = '_deploy/assets/index-DUcNPOLc-v840.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

CHIP = '{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,height:20,width:20,borderRadius:999,border:`1px solid #323b48`,background:`#20262f`,fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`}'

# ── the post ──
for v in ('e', 'c'):
    patch(t('(' + v + '.pinned||' + v + '.locked||' + v + '.browser_id&&String(' + v + '.browser_id).startsWith(`bot-`))&&'),
          t('(' + v + '.pinned||' + v + '.locked||' + v + '.frozen||' + v + '.browser_id&&String(' + v + '.browser_id).startsWith(`bot-`))&&'), 'badge row ' + v)
    patch(t('children:`🔒`}),' + v + '.browser_id&&String(' + v + '.bro'),
          t('children:`🔒`}),' + v + '.frozen&&(0,L.jsx)(`span`,{title:`Archived`,style:' + CHIP + ',children:`📦`}),' + v + '.browser_id&&String(' + v + '.bro'), 'archive badge ' + v)
patch(t('onClick:t=>{t.preventDefault(),t.stopPropagation(),i?i(e.id,r===1?0:1):'), t('onClick:t=>{t.preventDefault(),t.stopPropagation();if(e.frozen)return;i?i(e.id,r===1?0:1):'), 'no wings on cards')
patch(t('onClick:async t=>{if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}t.preventDefault();const _nv'),
      t('onClick:async t=>{if(c.frozen)return;if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}t.preventDefault();const _nv'), 'no wings on the post')
patch(t('ae&&n&&c.username===n&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{if(!confirm(`Are you sure?`))return;await fetch(`${R}/delete-my-post`'),
      t('ae&&n&&c.username===n&&!c.locked&&!c.frozen&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{if(!confirm(`Are you sure?`))return;await fetch(`${R}/delete-my-post`'), 'no self delete')
patch(t('N&&!c.archived&&!(c.is_admin&&t!==`admin`)&&'), t('N&&!c.frozen&&!(c.is_admin&&t!==`admin`)&&'), 'archive button')
patch(t('`Archive this post? It will be hidden from the feed but viewable in the admin panel.`))return;await zr({type:`archive_post`,post_id:c.id});o(`/`)}'),
      t('`Archive this post? It stays on the site but freezes: no new chirps, wings or reactions, and its author can\'t delete it.`))return;await zr({type:`archive_post`,post_id:c.id});await P()}'), 'archive message')
patch(t('N&&c.archived&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{await zr({type:`unarchive_post`'),
      t('N&&c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{await zr({type:`unarchive_post`'), 'unarchive button')

# ── the chat ──
patch(t('||c?.locked)return;let _fc='), t('||c?.locked||c?.frozen)return;let _fc='), 'no sending')
patch(t('!c.locked&&(0,L.jsxs)(`div`,{className:`chat-compose`,'),
      t('(c.locked||c.frozen)&&!_pv&&(0,L.jsx)(`div`,{style:{padding:`14px`,textAlign:`center`,color:`#64748b`,fontSize:13,fontWeight:600,borderTop:`1px solid rgba(148,163,184,0.1)`},children:c.frozen?`📦 Archived`:`🔒 Locked`}),!c.locked&&!c.frozen&&(0,L.jsxs)(`div`,{className:`chat-compose`,'), 'no compose')
patch(t('onReply:e=>C(e),onReact:ne,'), t('onReply:c.locked||c.frozen?void 0:e=>C(e),onReact:c.frozen?void 0:ne,'), 'no reply or react')
patch(t('(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1);if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}s&&s(e)},children:`Reply`}),(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:D,children:`React`})'),
      t('s&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1);if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}s&&s(e)},children:`Reply`}),c&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:D,children:`React`})'), 'hide reply and react')

# ── Mod Panel: lift Archived out of the Deleted card ──
a_mark = t(',(0,L.jsxs)(`div`,{style:{borderTop:`1px solid #2e303a`,marginTop:8},children:[(0,L.jsxs)(`div`,{style:{padding:`16px 20px`,borderBottom:_archOpen')
b_mark = t(']})]}),e&&(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,marginTop:16},children:[(0,L.jsxs)(`div`,{onClick:()=>A(e=>!e),')
if content.count(a_mark) != 1 or content.count(b_mark) != 1:
    errors.append('FAIL (archived block markers)')
else:
    a = content.index(a_mark); b = content.index(b_mark)
    block = content[a + 1:b]
    old_open = t('(0,L.jsxs)(`div`,{style:{borderTop:`1px solid #2e303a`,marginTop:8},children:[')
    assert block.startswith(old_open)
    block = t('(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16,display:_tb===`archived`?`block`:`none`},children:[') + block[len(old_open):]
    tail = b_mark[len(t(']})]}),')):]
    content = content[:a] + t(']})]}),') + block + ',' + t('_adm&&') + tail[len(t('e&&')):].replace(t('style:{padding:0,marginTop:16}'), t('style:{padding:0,marginTop:16,display:_tb===`bot`?`block`:`none`}'), 1) + content[b + len(b_mark):]
    print('OK: archived card')

# tabs
patch(t('[_tr,_setTr]=(0,_.useState)([]),'), t('[_tr,_setTr]=(0,_.useState)([]),[_tb,_setTb]=(0,_.useState)(`flock`),'), 'tab state')
patch(t('[p,m]=(0,_.useState)(!1),'), t('[p,m]=(0,_.useState)(!0),'), 'deleted open')
patch(t('[_archOpen,_setArchOpen]=(0,_.useState)(!1)'), t('[_archOpen,_setArchOpen]=(0,_.useState)(!0)'), 'archived open')
patch(t('children:null}),(()=>{let t=[...se.trim()?'),
      t('children:null}),(0,L.jsx)(`div`,{className:`mod-tabs`,style:{display:`flex`,gap:6,overflowX:`auto`,paddingBottom:2},children:[[`flock`,`Flock`,l.length],[`archived`,`Archived`,_archPosts.length],[`deleted`,`Deleted`,d.length],..._adm?[[`bot`,`Bot`,null]]:[]].map(([_k,_n,_c])=>(0,L.jsxs)(`button`,{type:`button`,onClick:()=>_setTb(_k),style:{flexShrink:0,padding:`8px 14px`,borderRadius:999,border:`1px solid `+(_tb===_k?`#c084fc`:`#2e303a`),background:_tb===_k?`#c084fc`:`transparent`,color:_tb===_k?`#14081d`:`#94a3b8`,fontWeight:700,fontSize:13,cursor:`pointer`},children:[_n,_c!==null&&(0,L.jsx)(`span`,{style:{marginLeft:6,opacity:.7,fontWeight:600},children:_c})]},_k))}),(()=>{let t=[...se.trim()?'),
      'tab bar')
patch(t('return(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16},children:[(0,L.jsxs)(`div`,{style:{padding:`14px 20px`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`},children:[(0,L.jsxs)(`h3`,{style:{margin:0,color:`#f8fafc`,fontSize:16,fontWeight:700,marginRight:`auto`},children:[`Flock `,'),
      t('return(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16,display:_tb===`flock`?`block`:`none`},children:[(0,L.jsxs)(`div`,{style:{padding:`14px 20px`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`},children:[(0,L.jsxs)(`h3`,{style:{margin:0,color:`#f8fafc`,fontSize:16,fontWeight:700,marginRight:`auto`},children:[`Flock `,'), 'flock card')
patch(t('(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16},children:[(0,L.jsxs)(`div`,{style:{padding:`14px 20px`,borderBottom:p?`1px solid #2e303a`:`none`,display:`flex`,alignItems:`center`,gap:10,cursor:`pointer`},onClick:()=>m(e=>!e),children:'),
      t('(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidden`,marginTop:16,display:_tb===`deleted`?`block`:`none`},children:[(0,L.jsxs)(`div`,{style:{padding:`14px 20px`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`},children:'), 'deleted card')
patch(t(',(0,L.jsx)(`span`,{style:{color:`#64748b`,fontSize:13},children:p?`▲`:`▼`})'), '', 'deleted arrow')
patch(t('borderBottom:_archOpen?`1px solid #2e303a`:`none`,display:`flex`,alignItems:`center`,gap:10,cursor:`pointer`},onClick:()=>_setArchOpen(e=>!e),children:'),
      t('borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10,flexWrap:`wrap`},children:'), 'archived header')
patch(t(',(0,L.jsx)(`span`,{style:{color:`#64748b`,fontSize:13},children:_archOpen?`▲`:`▼`})'), '', 'archived arrow')

# post rows
patch(t('display:`flex`,alignItems:`center`,gap:12},children:[(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0},children:[(0,L.jsx)(`div`,{style:{color:`#f8fafc`,fontWeight:600,fontSize:14,marginBottom:3,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:e.title||`—`}),'),
      t('display:`flex`,alignItems:`center`,gap:12,flexWrap:`wrap`},children:[_pvw(e).img&&(0,L.jsx)(`img`,{src:_pvw(e).img,alt:``,style:{width:52,height:52,borderRadius:8,objectFit:`cover`,flexShrink:0}}),(0,L.jsxs)(`div`,{style:{flex:1,minWidth:170},children:[(0,L.jsx)(`div`,{style:{color:`#f8fafc`,fontWeight:600,fontSize:14,marginBottom:3,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:_pvw(e).title}),'), 'row title', 2)
patch(t('e.content&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginTop:6,overflow:`hidden`,display:`-webkit-box`,WebkitLineClamp:2,WebkitBoxOrient:`vertical`},children:e.content})'),
      t('_pvw(e).text&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginTop:6,overflow:`hidden`,display:`-webkit-box`,WebkitLineClamp:2,WebkitBoxOrient:`vertical`},children:_pvw(e).text})'), 'row preview', 2)
BTN = '{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`}'
patch(t('(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`unarchive_post`,post_id:e.id}),_e()},style:' + BTN + ',children:`Restore`})'),
      t('(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`hide_archive`,post_id:e.id,hidden:!e.archived}),_e()},style:{padding:`6px 12px`,borderRadius:8,border:`1px solid #374151`,background:e.archived?`#3b2a52`:`transparent`,color:e.archived?`#c084fc`:`#94a3b8`,fontWeight:600,fontSize:12,cursor:`pointer`},children:e.archived?`Show to members`:`Hide from members`}),(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`unarchive_post`,post_id:e.id}),_e()},style:' + BTN + ',children:`Unarchive`})'), 'archive buttons')
patch(t('(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,flexShrink:0},children:[(0,L.jsx)(`a`,{href:`/post/${e.id}`,target:`_blank`,'),
      t('(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,flexWrap:`wrap`,maxWidth:`100%`},children:[(0,L.jsx)(`a`,{href:`/post/${e.id}`,target:`_blank`,'), 'buttons wrap', 2)
patch(t('\nfunction _Bd(){'),
      t('\nfunction _pvw(e){let{text:_t,attachment:_a,attachments:_s}=Mr(e.content||``),_x=(_t||``).trim();return{title:e.title||_a?.title||_x.slice(0,80)||`Untitled post`,text:e.title?_x||_a?.description||``:_a?.title?_a.description||_x:``,img:_s?.[0]?.url||(_a?.type===`image`?_a.url:_a?.image||_a?.poster)||null}}\nfunction _Bd(){'), 'preview helper')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
