#!/usr/bin/env python3
"""Patch v1261 -> v1262: mod flagging.
- Post page and chirp menus get a Flag button for mods and admins (not on mod/admin content or your own).
  Flagging asks for an optional reason, then the worker hides it, cages the author, logs it in Flagged and
  notifies the admins (worker /mod-action flag_post / flag_comment).
- Delete is admin-only now; a mod only sees Delete on their own post or chirp (the worker enforces this too).
- Flagged tab: lists mod flags with who flagged and why; only admins get Not bad / Confirm (mods see
  "Waiting for an admin")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1261.js'
dst = '_deploy/assets/index-DUcNPOLc-v1262.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HEAD = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
FLAG = HEAD + '<path d="M5 21V4"/><path d="M5 4.5c4.5-2.5 7.5 2.5 13 0v9c-5.5 2.5-8.5-2.5-13 0"/></svg>'
patch('function _ppIco(k){return ({', 'function _ppIco(k){return ({"FLAG": "%s", ' % FLAG.replace('"', '\\"'), 'flag icon')
# flag helper: like zr but tells the caller whether it worked
patch("async function zr(e){", "async function _ppFlag(e){try{let r=await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/mod-action`,{method:`POST`,headers:{\"Content-Type\":`application/json`,...$n()},body:JSON.stringify(e)}),x=await r.json().catch(()=>({}));if(!r.ok){alert(x.error||`Could not flag`);return!1}return!0}catch(e){alert(e.message);return!1}}async function zr(e){", 'flag helper')
FLAGQ = "`Flag this %s? It's hidden right away, ${%s||`the author`} goes to The Cage, and an admin reviews it.\\n\\nReason (optional):`"
# post page: Flag for mods/admins, Delete for admins (or a mod's own post)
patch("!c.frozen&&!(c.is_admin&&t!==`admin`)&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool danger`,onClick:async()=>{if(!confirm(`Are you sure?`))return;await zr({type:`delete_post`,post_id:c.id});o(`/`)}",
      "!c.frozen&&!c.is_admin&&!c.is_mod&&!(n&&c.username===n)&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool danger`,onClick:async()=>{const _r=prompt(" + FLAGQ % ('post', 'c.username') + ",``);if(_r===null)return;if(await _ppFlag({type:`flag_post`,post_id:c.id,reason:_r}))o(`/`)},children:[(0,L.jsx)(`span`,{className:`pp-ic mt-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`FLAG`)}}),`Flag`]}),"
      "!c.frozen&&(t===`admin`||!!n&&c.username===n)&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool danger`,onClick:async()=>{if(!confirm(`Are you sure?`))return;await zr({type:`delete_post`,post_id:c.id});o(`/`)}",
      'post page flag + admin delete')
# chirps
patch("myUsername:n,canDelete:!c.frozen&&(N&&(t===`admin`||!_e.is_admin)||ae&&!c.locked&&n&&_e.username===n)",
      "myUsername:n,canFlag:!c.frozen&&!!N&&!_e.is_admin&&!_e.is_mod&&!!_e.username&&_e.username!==n,onFlag:async()=>{const _r=prompt(" + FLAGQ % ('chirp', '_e.username') + ",``);if(_r===null)return;if(await _ppFlag({type:`flag_comment`,comment_id:_e.id,reason:_r}))await P()},"
      "canDelete:!c.frozen&&(N&&(t===`admin`||!!n&&_e.username===n)||ae&&!c.locked&&n&&_e.username===n)", 'chirp flag + admin delete')
patch("myUsername:_myUn=null,canDelete:r,onDelete:i,", "myUsername:_myUn=null,canFlag:_cfl=!1,onFlag:_ofl,canDelete:r,onDelete:i,", 'chirp props')
patch("r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},children:`Delete`})",
      "_cfl&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),y(!1),_ofl&&_ofl()},children:`Flag`}),r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},children:`Delete`})", 'chirp Flag button')
# Flagged tab
patch("f.status===`open`?[(0,L.jsx)(`button`",
      "f.status===`open`&&!d.can_review?(0,L.jsx)(`span`,{className:`af-done`,children:`Waiting for an admin`}):f.status===`open`?[(0,L.jsx)(`button`", 'mods cannot review')
patch("children:`Flagged by the AI check`}", "children:`Flagged by mods and the AI check`}", 'tab title')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
