#!/usr/bin/env python3
"""Patch v946 -> v947: busy chirps stay compact.
- Reaction pills under a chirp are one row: sorted by count (most used first), as many as fit the bubble's
  width, then a "+N" pill (N = hidden emoji kinds) that opens the who-reacted sheet on All. Your own
  reaction is always kept visible. Refits on every render and on window resize.
- The open chirp menu lists at most 5 birds (you first if you reacted), then "+N more" -> the same sheet."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v946.js'
dst = '_deploy/assets/index-DUcNPOLc-v947.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,children:ee.map(([t,n])=>',
      'ee.length>0&&(0,L.jsxs)(`div`,{className:`chat-reactions rx-fit`,ref:el=>{el&&_rxFit(el)},children:[..._rxSort(ee).map(([t,n])=>',
      'row: sorted + fit')
patch('children:[t,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:n.length})]},t))}),v&&',
      'children:[t,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:n.length})]},t)),'
      '(0,L.jsx)(`button`,{type:`button`,className:`chat-reaction-pill rx-more`,"aria-label":`See all reactions`,onClick:ev=>{ev.stopPropagation();_setRxW(`all`)}},`__more`)]}),v&&',
      'row: +N pill')
patch('function _rxWho(ee,only,go){const rows=_rxGroup(ee,only);if(!rows.length)return null;',
      'function _rxWho(ee,only,go,more){let rows=_rxGroup(ee,only);if(!rows.length)return null;'
      'const _mn=Qn()?.username;if(_mn){const k=rows.findIndex(r=>r.name===_mn);if(k>0)rows=[rows[k],...rows.slice(0,k),...rows.slice(k+1)]}'
      'const _extra=rows.length>5?rows.length-5:0;if(_extra)rows=rows.slice(0,5);',
      'menu: cap 5')
patch('children:[...rows.map((r,i)=>_rxRow(r,i,0,1,go))]})}',
      'children:[...rows.map((r,i)=>_rxRow(r,i,0,1,go)),_extra?(0,L.jsx)(`button`,{type:`button`,className:`rx-row rx-morerow`,onClick:ev=>{ev.stopPropagation();more&&more()},children:`+${_extra} more`},`more`):null]})}',
      'menu: +N more')
patch('...ee.map(([q,ids])=>tab(q,`${q} ${ids.length}`))', '..._rxSort(ee).map(([q,ids])=>tab(q,`${q} ${ids.length}`))', 'sheet tabs sorted')
patch('_rxWho(ee,null,_rxGo)', '_rxWho(ee,null,_rxGo,()=>_setRxW(`all`))', 'menu: more opens sheet')

c += r'''
function _rxSort(ee){return ee.map((x,i)=>[x,i]).sort((a,b)=>b[0][1].length-a[0][1].length||a[1]-b[1]).map(x=>x[0])}
function _rxFit(row){requestAnimationFrame(()=>{if(!row.isConnected)return;
 const m=row.querySelector(`.rx-more`);if(!m)return;
 const ps=[...row.querySelectorAll(`.chat-reaction-pill:not(.rx-more)`)];
 ps.forEach(p=>{p.style.display=``;p.style.order=``});m.style.display=`none`;m.style.order=``;
 const cs=getComputedStyle(row),W=row.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight),g=parseFloat(cs.columnGap)||4;
 const w=ps.map(p=>p.offsetWidth),tot=w.reduce((a,b)=>a+b,0)+g*(ps.length-1);
 if(tot<=W+.5)return;
 m.style.display=`inline-flex`;m.setAttribute(`data-more`,`+`+ps.length);const mw=m.offsetWidth;
 let used=mw,vis=[];for(let i=0;i<ps.length;i++){if(used+w[i]+g<=W+.5){vis.push(i);used+=w[i]+g}else break}
 const mi=ps.findIndex(p=>p.classList.contains(`mine`));
 if(mi>=0&&!vis.includes(mi)){while(vis.length&&used+w[mi]+g>W+.5){used-=w[vis.pop()]+g}vis.push(mi);ps[mi].style.order=`1`}
 ps.forEach((p,i)=>{if(!vis.includes(i))p.style.display=`none`});
 m.style.order=`2`;m.setAttribute(`data-more`,`+`+(ps.length-vis.length))})}
try{let _rxRz=0;window.addEventListener(`resize`,()=>{cancelAnimationFrame(_rxRz);_rxRz=requestAnimationFrame(()=>document.querySelectorAll(`.chat-reactions.rx-fit`).forEach(_rxFit))})}catch(e){}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.chat-reactions.rx-fit{flex-wrap:nowrap;overflow:hidden}
.chat-reactions.rx-fit .chat-reaction-pill{flex-shrink:0}
.chat-reaction-pill.rx-more{display:none;color:#94a3b8;font-weight:700;font-size:11px}
.chat-reaction-pill.rx-more::after{content:attr(data-more)}
.rx-morerow{justify-content:center;width:100%;background:rgba(148,163,184,.06);border:1px solid rgba(148,163,184,.18);color:#94a3b8;font-size:12px;font-weight:700;font-family:inherit;cursor:pointer}
.rx-morerow:active{filter:brightness(1.3)}
.rx-tabs{flex-shrink:0}
.rx-list{min-height:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
