#!/usr/bin/env python3
"""Patch v1005 -> v1006: a huddle can start with an opening message.
- New Post → Huddles: under the title there's a box ("Start the conversation… optional, it gets pinned") and the
  photo/video button. Whatever you write/attach becomes your first chirp in the huddle, pinned.
- Invites show the first line of it under the invite ("…" after ~80 characters, 📷 Photo / 🎬 Video for media only)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1005.js'
dst = '_deploy/assets/index-DUcNPOLc-v1006.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("!_isHuddle&&(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),placeholder:T?`Add a caption (optional)…`:`What's going on?`",
      "(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),placeholder:_isHuddle?`Start the conversation…`:T?`Add a caption (optional)…`:`What's going on?`",
      'body box for huddles')
patch('!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>ie.current?.click(),className:`feed-post-action-pill`',
      '(0,L.jsx)(`button`,{type:`button`,onClick:()=>ie.current?.click(),className:`feed-post-action-pill`', 'photo/video for huddles')
patch('huddle_members:_isHuddle?',
      'first_chirp:_isHuddle&&(s.trim()||T)?(T?T.type===`images`?s+_amk+JSON.stringify(T.urls.map(_u=>({type:`image`,url:_u})))+`]`:s+jr+JSON.stringify(T)+`]`:s):null,huddle_members:_isHuddle?',
      'send opening chirp')
patch('w.rest]:w.rest});', 'w.rest,_nPrev(e)]:[w.rest,_nPrev(e)]});', 'invite preview line')
patch('c.is_huddle&&Array.isArray(e)&&e.length>0?(0,L.jsx)(_HxRow,{post:c,members:e})',
      'c.is_huddle&&Array.isArray(e)?(0,L.jsx)(_HxRow,{post:c,members:e})', 'member row even before anyone accepts')
patch('children:`${all.length} birds`+', 'children:`${all.length} bird${all.length===1?``:`s`}`+', '1 bird')
patch("(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),placeholder:_isHuddle?",
      "_isHuddle&&(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,margin:`14px 0 6px`},children:`Opening message (optional, it gets pinned):`}),(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),placeholder:_isHuddle?",
      'label for the message box')
c += r'''
function _nPrev(e){return e&&e.req&&e.preview?(0,L.jsx)(`div`,{className:`n-prev`,children:`“${e.preview}”`},`pv`):null}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.n-prev{margin-top:4px;font-size:12.5px;line-height:1.4;color:#94a3b8;font-style:italic;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
