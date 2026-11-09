#!/usr/bin/env python3
"""Patch v938 -> v939: notifications as big muted user pills.
Each row is a rounded pill tinted (muted) in the colour of the bird it's about, with that bird's emoji
(colour filter + sparkles, admin hat) in a circle and the notification type (💬 🪽 👥 😊 …) as a small badge.
The bird's name is bold in their colour, the rest muted, time on the right. Unread = stronger tint + thin
outline; read = faint tint. Colours: bird -> their colour; admin -> soft white; mod -> purple;
Extinct Bird -> dark grey with the grey 🐦; no bird ("You …", system) -> muted site purple with 🔔.
The actor is read from the notification text (first word), as the colour bars did before."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v938.js'
dst = '_deploy/assets/index-DUcNPOLc-v939.js'
c = open(src, encoding='utf-8').read()
old = ("onClick:()=>{_nMark(e);a()},style:{display:`flex`,alignItems:`flex-start`,gap:12,padding:`12px 18px`,textDecoration:`none`,borderBottom:`1px solid #2e303a`,background:t?`color-mix(in srgb, ${_ncol(e.text)} 10%, transparent)`:`transparent`,borderLeft:`3px solid ${_ncol(e.text)}`},children:[(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1,flexShrink:0},children:e.icon}),(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0},children:[(0,L.jsx)(`div`,{style:{color:t?`#f8fafc`:`#94a3b8`,fontSize:13,lineHeight:1.4},children:e.text}),(0,L.jsx)(`div`,{style:{color:`#475569`,fontSize:11,marginTop:3},children:Un(e.time)})]})]},e.id)})")
new = "onClick:()=>{_nMark(e);a()},style:_nPillStyle(e,t),children:_nPillKids(e,t)},e.id)})"
if c.count(old) != 1: print('FAIL row', c.count(old)); sys.exit(1)
c = c.replace(old, new)
JS = r'''
function _nWho(e){const tx=String(e&&e.text||'');
 if(/^Extinct Bird\b/.test(tx))return{kind:'extinct',col:'#6b7280',name:'Extinct Bird',rest:tx.slice(12),bird:{e:'🐦',f:'grayscale(1) opacity(.75)',s:null}};
 const w=tx.split(' ')[0];
 if(!w||w==='You'||w==='Someone')return{kind:'system',col:'#c084fc',name:null,rest:tx,bird:null};
 const l=w.toLowerCase(),adm=_adminUsers.has(l);
 return{kind:'bird',col:_ncol(tx),name:w,rest:tx.slice(w.length),bird:Jn({username:w,browser_id:null,is_admin:adm,is_mod:_modUsers.has(l)})}}
function _nPillStyle(e,t){const w=_nWho(e),c=w.col;
 return{display:`flex`,alignItems:`center`,gap:12,margin:`6px 10px`,padding:`10px 14px 10px 10px`,borderRadius:20,textDecoration:`none`,
  background:`color-mix(in srgb, ${c} ${t?16:7}%, #15171d)`,border:`1px solid color-mix(in srgb, ${c} ${t?45:12}%, transparent)`,transition:`background .2s, border-color .2s`}}
function _nPillKids(e,t){const w=_nWho(e),c=w.col,b=w.bird;
 const face=b&&b.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:24,height:24,objectFit:`contain`}})
  :b?(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`,justifyContent:`center`,fontSize:21,lineHeight:1},children:[(0,L.jsx)(`span`,{style:b.f?{filter:b.f}:{},children:b.e||`🐦`}),...(b.s?_spEls(b.s,20):[])]})
  :(0,L.jsx)(`span`,{style:{fontSize:19,lineHeight:1},children:`🔔`});
 const avatar=(0,L.jsxs)(`div`,{style:{position:`relative`,flexShrink:0,width:38,height:38,borderRadius:999,display:`flex`,alignItems:`center`,justifyContent:`center`,background:`color-mix(in srgb, ${c} 26%, #1b1d24)`,border:`1px solid color-mix(in srgb, ${c} 40%, transparent)`},children:[face,
  w.kind!=='system'&&e.icon?(0,L.jsx)(`span`,{style:{position:`absolute`,right:-5,bottom:-4,minWidth:18,height:18,borderRadius:999,background:`#1b1d24`,border:`1px solid #2e303a`,display:`flex`,alignItems:`center`,justifyContent:`center`,fontSize:10,lineHeight:1,padding:`0 2px`,boxSizing:`border-box`},children:e.icon}):null]});
 const txt=(0,L.jsx)(`div`,{style:{flex:1,minWidth:0,fontSize:13,lineHeight:1.4,color:t?`#cbd5e1`:`#8b98a9`,textAlign:`left`},children:w.name?[(0,L.jsx)(`span`,{style:{fontWeight:700,color:c===`#ffffff`?`#e5e7eb`:c},children:w.name},`n`),w.rest]:w.rest});
 const time=(0,L.jsx)(`div`,{style:{flexShrink:0,alignSelf:`flex-start`,marginTop:2,color:`#566275`,fontSize:11,whiteSpace:`nowrap`},children:Un(e.time)});
 return[avatar,txt,time]}
'''
open(dst, 'w', encoding='utf-8').write(c + JS); print('Wrote ' + dst)
