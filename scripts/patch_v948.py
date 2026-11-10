#!/usr/bin/env python3
"""Patch v947 -> v948: pinned chirps keep their place in the chat.
- Full chat: the timeline is purely chronological; a pinned chirp stays where it was said (with its 📌 on the
  name bar, no glow). Pinned copies (with the glow) still sit at the top of the chat under a "📌 Pinned"
  title, newest first, max 3 shown + a "📌 N more pinned" pill that expands / "Show less".
- Tapping a pinned copy's bubble jumps to the original (loads older chirps if needed) and glows it.
  Its name bar still opens the actions (react, unpin, ...), which act on the same chirp.
- A pinned chirp older than the loaded part of the chat isn't dropped into the timeline next to unrelated
  chirps; it appears there once older chirps are loaded (the jump does that).
- Preview (post page): unchanged look; tapping a pinned chirp opens the chat focused on the original."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v947.js'
dst = '_deploy/assets/index-DUcNPOLc-v948.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# Chronological order (pinned no longer floated by the sort)
patch('de=[...ue].sort((e,t)=>{if(e.pinned&&!t.pinned)return-1;if(!e.pinned&&t.pinned)return 1;let n=',
      'de=[...ue].sort((e,t)=>{let n=', 'sort: chronological')

# One builder for chirps, used for timeline items and pinned copies
s0 = '_rev.forEach((_e,_i)=>{_out.push('
s = c.find(s0)
if s < 0 or c.count(s0) != 1: print('FAIL forEach'); sys.exit(1)
s += len(s0)
e = c.find(',_e.id));let _next=_rev[_i+1]', s)
rcall = c[s:e]
if not rcall.startswith('(0,L.jsx)(Rr,{comment:_e,'): print('FAIL rcall'); sys.exit(1)
builder = 'const _R=(_e,_pc,_k,_px)=>' + rcall.replace('(0,L.jsx)(Rr,{comment:_e,', '(0,L.jsx)(Rr,{pinCopy:_pc,pinX:_px,comment:_e,', 1) + ',_k);'
c = c[:s] + '_R(_e,!!(_pv&&_e.pinned),_e.id));let _next=_rev[_i+1]' + c[e+len(',_e.id));let _next=_rev[_i+1]'):]
print('OK: builder')

patch('_rev=[..._ls,..._ps]}_rev.forEach((_e,_i)=>{_out.push(_R(',
      '_rev=[..._ls,..._ps]}' + builder +
      'let _pins=[];if(!_pv){_pins=_rev.filter(x=>x.pinned);let _t0=_rev.filter(x=>!x.pinned).map(x=>new Date(x.created_at).getTime()),_mn=_t0.length?Math.min(..._t0):0;'
      '_rev=_rev.filter(x=>!x.pinned||!_hmR.current||new Date(x.created_at).getTime()>=_mn)}'
      '_rev.forEach((_e,_i)=>{_out.push(_R(',
      'pins split out in full chat')

patch('_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));return _out;',
      'if(!_pv&&_pins.length){let _p2=[..._pins].sort((a,b)=>new Date(b.created_at)-new Date(a.created_at)),_ex=_p2.length-3;'
      'if(_ex>0)_out.push((0,L.jsx)(`button`,{type:`button`,className:`pin-more`,"data-n":_ex,onClick:ev=>{ev.stopPropagation();D.current&&D.current.classList.toggle(`pins-open`)}},`pinmore`));'
      'for(let k=_p2.length-1;k>=0;k--)_out.push(_R(_p2[k],!0,`pc-`+_p2[k].id,k>=3));'
      '_st(`📌 Pinned`,_p2[0].created_at)}'
      '_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));return _out;',
      'pinned copies on top')

# Chirp: copy vs original
patch('function Rr({comment:e,', 'function Rr({pinCopy:_pc=!1,pinX:_px=!1,comment:e,', 'Rr props')
patch('"data-comment-id":e.id,children:(0,L.jsxs)(`div`,{className:`chat-msg-body${e.pinned?` chat-pinned`:``}`',
      '"data-comment-id":_pc?void 0:e.id,"data-pin-of":_pc?e.id:void 0,"data-pin-x":_px?1:void 0,children:(0,L.jsxs)(`div`,{className:`chat-msg-body${e.pinned&&_pc?` chat-pinned`:``}`',
      'Rr: ids + glow only on copy')
patch('className:`chat-bubble${p?` pending`:``}`,onClick:()=>!p&&y(e=>!e),',
      'className:`chat-bubble${p?` pending`:``}`,onClick:()=>{if(_pc&&d){y(!1);d(e.id);return}!p&&y(e=>!e)},',
      'Rr: copy bubble jumps')

# Preview: tapping a pinned chirp focuses the original in the chat
patch('_fid.current=_tg.closest(`.chat-msg`)?.dataset.commentId||null',
      '_fid.current=_tg.closest(`.chat-msg`)?.dataset.commentId||_tg.closest(`.chat-msg`)?.dataset.pinOf||null',
      'preview focus')

c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.chat-window:not(.pins-open) [data-pin-x]{display:none}
.pin-more{align-self:center;flex-shrink:0;margin:2px auto 8px;height:26px;padding:0 12px;border-radius:999px;border:1px solid rgba(148,163,184,.2);background:rgba(148,163,184,.07);color:#94a3b8;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit}
.pin-more::after{content:"📌 " attr(data-n) " more pinned"}
.chat-window.pins-open .pin-more::after{content:"Show less"}
[data-pin-of] .chat-bubble{cursor:pointer}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
