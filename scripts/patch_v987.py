#!/usr/bin/env python3
"""Patch v986 -> v987: chirp preview filter.
Next to the 💬 count on the post page, a "✨ Highlights ▾" pill (replacing the faded "Chirp preview" label)
opens a small menu:
  ✨ Highlights  (default)  Pinned -> Top chirps -> Most replied, else Latest (as before)
  🔥 Top                    the 5 most reacted chirps
  ↩️ Most replied           the 5 chirps with the most replies
  🕒 Latest                 the 5 newest chirps
  🖼️ Media                  the 5 newest chirps with photos or videos
Only Highlights shows the pinned section. Empty views say so ("No photos or videos yet"...). The choice resets
to Highlights on each post. Tapping a chirp still opens the chat at it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v986.js'
dst = '_deploy/assets/index-DUcNPOLc-v987.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('[_ldO,_setLdO]=(0,_.useState)(!1),', '[_ldO,_setLdO]=(0,_.useState)(!1),[_cpm,_setCpm]=(0,_.useState)(`hl`),', 'mode state')
patch('_cfR.current=!1;_ckR.current=null;_setCF(!1);', '_cfR.current=!1;_ckR.current=null;_setCF(!1);_setCpm(`hl`);', 'reset per post')
patch('let _tg=_ev.target;if(_tg.closest(`.chat-bubble`)&&', 'let _tg=_ev.target;if(_tg.closest(`.cp-filter`))return;if(_tg.closest(`.chat-bubble`)&&', 'filter button not swallowed')
patch('let _nl=0,_np=0,_pmo=0,_tpOn=!1,_nR=0,', 'let _nl=0,_np=0,_pmo=0,_tpOn=!1,_nR=0,_cpT=null,_cpD=!1,', 'vars')
patch('if(_pv){_pmo=_rev.filter(_x=>_x.pinned).length-3;const _tpl=',
      'if(_pv&&_cpm!==`hl`){_pmo=0;_np=0;_nR=0;'
      'const _src=_cpm===`top`?(_cpTop[r]||[]).slice(0,5):_cpm===`rep`?(_cpRep[r]||[]).slice(0,5):_cpm===`media`?_rev.filter(_x=>/\\[ATTACH/.test(_x.content||``)).slice(0,5):_rev.slice(0,5);'
      '_tpOn=_cpm===`top`||_cpm===`rep`;_cpT=_CPL[_cpm];_cpD=!_tpOn;const _l2=_tpOn?[..._src].reverse():_src;_nl=_l2.length;_rev=_l2}'
      'else if(_pv){_pmo=_rev.filter(_x=>_x.pinned).length-3;const _tpl=',
      'build the chosen view')
patch('if(_i===_nl-1&&_nl>_nR)_st(_tpOn?`🔥 Top chirps`:`🕒 Latest`,_tpOn?null:_e.created_at);',
      'if(_i===_nl-1&&_nl>_nR)_st(_cpT||(_tpOn?`🔥 Top chirps`:`🕒 Latest`),_cpT?(_cpD?_e.created_at:null):(_tpOn?null:_e.created_at));',
      'section title')
patch('_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));',
      '_pv&&_cpm!==`hl`&&!_nl&&de.length>0&&_out.push((0,L.jsx)(`div`,{className:`cp-empty`,children:_CPE[_cpm]},`cpe`));_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));',
      'empty view message')
patch('_pv&&(0,L.jsx)(`span`,{className:`cp-label`,children:`Chirp preview`})',
      '_pv&&(0,L.jsx)(`button`,{type:`button`,className:`cp-filter`,"aria-label":`Chirp preview: ${_CPL[_cpm]}`,onClick:ev=>{ev.stopPropagation();ev.preventDefault();_cpMenu(ev.currentTarget,_cpm,_setCpm)},children:[_CPL[_cpm].replace(` chirps`,``),(0,L.jsx)(`span`,{className:`cp-caret`,children:`▾`},`c`)]})',
      'filter pill')

c += r'''
const _CPL={hl:`✨ Highlights`,top:`🔥 Top`,rep:`↩️ Most replied`,latest:`🕒 Latest`,media:`🖼️ Media`};
const _CPE={top:`No reactions yet`,rep:`No replies yet`,latest:`No chirps yet`,media:`No photos or videos yet`};
function _cpMenu(btn,cur,set){document.querySelectorAll(`.cp-menu`).forEach(x=>x.remove());
 const m=document.createElement(`div`);m.className=`cp-menu`;m.setAttribute(`role`,`menu`);
 Object.entries(_CPL).forEach(([k,lb])=>{const b=document.createElement(`button`);b.type=`button`;b.className=`cp-opt`+(k===cur?` on`:``);b.textContent=lb;b.setAttribute(`role`,`menuitemradio`);b.setAttribute(`aria-checked`,k===cur?`true`:`false`);
  b.onclick=e=>{e.stopPropagation();set(k);close()};m.append(b)});
 document.body.append(m);const r=btn.getBoundingClientRect();
 m.style.left=Math.max(8,Math.min(r.left,innerWidth-m.offsetWidth-8))+`px`;m.style.top=(r.bottom+6)+`px`;
 requestAnimationFrame(()=>m.classList.add(`in`));
 const close=()=>{m.remove();document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`scroll`,close,!0)};
 const out=e=>{if(!m.contains(e.target)&&e.target!==btn&&!btn.contains(e.target))close()};
 setTimeout(()=>{document.addEventListener(`pointerdown`,out,!0);addEventListener(`scroll`,close,!0)},0)}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.cp-filter{display:inline-flex;align-items:center;gap:4px;height:26px;margin-left:8px;padding:0 10px;border-radius:999px;border:1px solid rgba(148,163,184,.22);background:rgba(148,163,184,.06);color:#94a3b8;font-size:12px;font-weight:700;font-family:inherit;cursor:pointer;white-space:nowrap;-webkit-tap-highlight-color:transparent}
.cp-filter:active{background:rgba(148,163,184,.14)}
.cp-caret{font-size:10px;opacity:.8}
.cp-menu{position:fixed;z-index:1002;min-width:180px;padding:6px;border-radius:14px;background:#1b1d24;border:1px solid #2e303a;box-shadow:0 12px 34px rgba(0,0,0,.5);display:flex;flex-direction:column;gap:2px;opacity:0;transform:translateY(-4px);transition:opacity .15s,transform .15s}
.cp-menu.in{opacity:1;transform:none}
.cp-opt{display:block;width:100%;text-align:left;padding:9px 12px;border:0;border-radius:10px;background:none;color:#e2e8f0;font-size:14px;font-weight:600;font-family:inherit;cursor:pointer}
.cp-opt:hover,.cp-opt:active{background:rgba(148,163,184,.1)}
.cp-opt.on{background:rgba(192,132,252,.16);color:#e9d5ff}
.cp-empty{align-self:center;flex-shrink:0;padding:18px 12px;color:#64748b;font-size:13px;text-align:center}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
