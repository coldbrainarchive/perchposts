#!/usr/bin/env python3
"""Patch v1014 -> v1015: photo tray on New Post + new media/link buttons + landing flash for media chirps.
- The chat's photo tray is shared: each place (chat, New Post) has its own tray store so they never mix.
- New Post: photos/videos show instantly with progress rings, drag to reorder, ✕, + tile, Retry;
  Post / Start huddle waits for uploads ("Uploading…").
- New Post buttons: the "📎 Media" and "🔗 Link" pills become the chat's circle + button and a matching circle
  link button, side by side in one pill. The link one toggles the link box (no separate Cancel pill).
- Media chirps now get the same colour flash + glow ring as text chirps when they land."""
import sys, re
src = '_deploy/assets/index-DUcNPOLc-v1014.js'
dst = '_deploy/assets/index-DUcNPOLc-v1015.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def cut(start_marker, end_marker, new, label):
    global c
    if c.count(start_marker) != 1: print('FAIL start', label, c.count(start_marker)); sys.exit(1)
    s = c.find(start_marker); e = c.find(end_marker, s)
    if e < 0 or e - s > 6000: print('FAIL end', label); sys.exit(1)
    c = c[:s] + new + c[e + len(end_marker):]; print('OK:', label, e - s)

# ---- take the v1014 tray code out of the bundle; it comes back below, per-store ----
old_block_src = open('scripts/patch_v1014.py', encoding='utf-8').read().split("c += r'''", 1)[1].rsplit("'''", 1)[0]
if c.count(old_block_src) != 1: print('FAIL old block', c.count(old_block_src)); sys.exit(1)
c = c.replace(old_block_src, ''); print('OK: v1014 tray code removed')

b = old_block_src
def r(old, new, n=None):
    global b
    k = b.count(old)
    if k == 0 or (n is not None and k != n): print('FAIL block', old[:60], k); sys.exit(1)
    b = b.replace(old, new)
r('const _mtS={items:[],gen:0,last:null,ls:new Set(),setCA:null,setUL:null,run:0,q:[]};',
  'function _mtMk(fmt){return{fmt,items:[],gen:0,last:null,ls:new Set(),setCA:null,setUL:null,run:0,q:[]}}\nconst _mtChat=_mtMk(`chat`),_mtNew=_mtMk(`post`);')
b = re.sub(r'_mtS(?![A-Za-z0-9_])', 'S', b)
for nm in ['_mtEmit', '_mtSync', '_mtReset', '_mtPump']:
    b = b.replace(nm + '()', nm + '(S)')
r('_mtFrom(ca)', '_mtFrom(S,ca)')
r('_mtUpload(it)', '_mtUpload(S,it)')
r('_mtUpload(x)', '_mtUpload(S,x)', 1)
r('function _mtQ(it)', 'function _mtQ(S,it)', 1)
r('nw.forEach(_mtQ)', 'nw.forEach(x=>_mtQ(S,x))', 1)
r('function _mtPick(files,setCA,setUL)', 'function _mtPick(S,files,setCA,setUL)', 1)
r('function _mtRemove(id)', 'function _mtRemove(S,id)', 1)
r('_mtRemove(x.id)', '_mtRemove(S,x.id)', 1)
r('function _mtDrag(row)', 'function _mtDrag(S,row)', 1)
r('_mtDrag(r)', '_mtDrag(S,r)', 1)
r('function _MTray({ca,setCA,setUL,pick})', 'function _MTray({st:S,ca,setCA,setUL,pick})', 1)
# New Post keeps its own format: photos are always a list
r(':it.length===1?{type:`image`,url:it[0].url}:', ':it.length===1&&S.fmt===`chat`?{type:`image`,url:it[0].url}:', 1)
# a link attachment on New Post is not the tray's business
r('if(ca===S.last)return;if(!ca)_mtReset(S);else _mtFrom(S,ca)},[ca]);',
  'if(ca===S.last)return;if(!ca)_mtReset(S);else if(/^(image|images|video)$/.test(ca.type))_mtFrom(S,ca);else if(S.items.length)_mtReset(S)},[ca]);', 1)
r('document.querySelectorAll(`.mt-row .mt-tile`)', 'document.querySelectorAll(`.chat-compose .mt-row .mt-tile`)', 1)
# landing: same colour flash + glow ring as text chirps
s0 = b.find('try{nb.animate([{boxShadow:'); e0 = b.find('catch(e){}', s0) + len('catch(e){}')
if s0 < 0: print('FAIL glow'); sys.exit(1)
b = b[:s0] + (
 'try{const bd=nb.closest(`.chat-msg-body`)||nb,br=bd.getBoundingClientRect(),G=`0 0 0 4px rgba(${C},0.6),0 0 20px rgba(${C},0.8)`,NG=`0 0 0 0px rgba(${C},0),0 0 0px rgba(${C},0)`;'
 'const o=document.createElement(`div`);o.className=`mt-flash`;Object.assign(o.style,{left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:getComputedStyle(bd).borderTopLeftRadius||`18px`});'
 'document.body.appendChild(o);window._follow&&window._follow(o,bd,document.querySelector(`.chat-window`));'
 'o.animate([{background:`rgba(${C},0.7)`,boxShadow:G},{background:`rgba(${C},0.55)`,boxShadow:G,offset:.18},{background:`rgba(${C},0)`,boxShadow:G,offset:.5},{background:`rgba(${C},0)`,boxShadow:NG}],{duration:2200,easing:`ease-out`,fill:`forwards`}).onfinish=()=>o.remove()}catch(e){}'
) + b[e0:]
b = b.replace('.mt-ghost{position:fixed;', '.mt-flash{position:fixed;z-index:2147482999;pointer-events:none;box-sizing:border-box}\n.mt-ghost{position:fixed;')
c += b
print('OK: tray code re-added per store')

# ---- chat call sites ----
patch('_mtPick([..._fe.target.files],_setCA,_setCUL)', '_mtPick(_mtChat,[..._fe.target.files],_setCA,_setCUL)', 'chat pick')
patch('(0,L.jsx)(_MTray,{ca:_cA,', '(0,L.jsx)(_MTray,{st:_mtChat,ca:_cA,', 'chat tray')

# ---- New Post ----
cut('onChange:e=>{const _fs=[...e.target.files];e.target.value=``;if(!_fs.length)return;if(_fs.length===1&&_fs[0].type.startsWith(`video`))',
    '}}}),(0,L.jsxs)(`div`,{className:`feed-post-actions`',
    'onChange:e=>{const _fs=[...e.target.files];e.target.value=``;_mtPick(_mtNew,_fs,E,re)}}),(0,L.jsxs)(`div`,{className:`feed-post-actions`', 'new post picker')
patch('T&&(0,L.jsxs)(`div`,{style:{marginTop:10,position:`relative`},children:[T.type===`images`',
      '(0,L.jsx)(_MTray,{st:_mtNew,ca:T,setCA:E,setUL:re,pick:()=>ie.current?.click()}),T&&!/^(image|images|video)$/.test(T.type)&&(0,L.jsxs)(`div`,{style:{marginTop:10,position:`relative`},children:[T.type===`images`',
      'new post tray')
PLUS = '(0,L.jsx)(`svg`,{width:12,height:12,viewBox:`0 0 12 12`,stroke:`currentColor`,strokeWidth:1.8,strokeLinecap:`round`,fill:`none`,style:{display:`block`},children:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`line`,{x1:6,y1:1.5,x2:6,y2:10.5}),(0,L.jsx)(`line`,{x1:1.5,y1:6,x2:10.5,y2:6})]})})'
LINK = '(0,L.jsxs)(`svg`,{width:16,height:16,viewBox:`0 0 24 24`,stroke:`currentColor`,strokeWidth:2.2,strokeLinecap:`round`,strokeLinejoin:`round`,fill:`none`,style:{display:`block`},children:[(0,L.jsx)(`path`,{d:`M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.5 1.5`}),(0,L.jsx)(`path`,{d:`M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.5-1.5`})]})'
TOOLS = ('(()=>{const _hm=!!(T&&/^(image|images|video)$/.test(T.type)),_hl=!!(T&&!_hm);return(0,L.jsxs)(`div`,{className:`np-tools`,children:['
         '(0,L.jsx)(`button`,{type:`button`,className:`np-tool`+(_hm||ne?` on`:``),disabled:ee===`link`||_hl,"aria-label":`Add photos or video`,title:`Photos or video`,onClick:()=>ie.current?.click(),children:' + PLUS + '}),'
         '!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,className:`np-tool`+(ee===`link`||_hl?` on`:``),disabled:_hm||ne,"aria-label":ee===`link`?`Close link box`:`Add a link`,title:`Link`,onClick:()=>{if(ee===`link`){D(null),k(``)}else D(`link`)},children:' + LINK + '})]})})(),')
cut('!T&&ee!==`link`&&(0,L.jsxs)(L.Fragment,{children:[!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>D(`link`)',
    'className:`feed-post-action-pill`,children:`Cancel`}),', TOOLS, 'new post buttons')
patch('(0,L.jsx)(`button`,{onClick:ae,disabled:l,className:`feed-post-action-pill`',
      '(0,L.jsx)(`button`,{onClick:ne?void 0:ae,disabled:l||ne,className:`feed-post-action-pill`', 'post waits for uploads')
patch('children:l?`Sending…`:_isHuddle?`Start huddle`:`Post`', 'children:ne?`Uploading…`:l?`Sending…`:_isHuddle?`Start huddle`:`Post`', 'uploading label')

c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.np-tools{display:inline-flex;align-items:center;gap:4px;padding:3px;border-radius:999px;border:1px solid #2e303a;background:rgba(255,255,255,.03)}
.np-tool{width:36px;height:36px;flex-shrink:0;border-radius:999px;border:none;background:rgba(255,255,255,.08);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;transition:background .15s,color .15s,opacity .15s;-webkit-tap-highlight-color:transparent}
.np-tool.on{background:var(--me,#c084fc);color:#14081d}
.np-tool:disabled{opacity:.35;cursor:default}
.np-card .mt-wrap,.nh-card .mt-wrap{padding:10px 0 0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
