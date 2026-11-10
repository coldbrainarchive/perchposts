#!/usr/bin/env python3
"""Patch v992 -> v993: huddles look and work like a messages inbox.
- Huddle cards (Huddles space): title, time of the last chirp, an unread count badge, a row of member circles
  (birds who chirped since you last read are lit up with their colour and a glow, the rest are faded, the owner
  has a 👑), and the last chirp as a one-line preview. Unread huddles are tinted and glow like unread
  notifications. Tapping the card opens the chat. No owner pill / HUDDLES tag / "Huddle with:" / footer.
- Huddle page: the "Huddle with:" pill list becomes one row (member circles + names); tapping it opens a
  Members sheet listing every bird (owner, you), and tapping a bird opens their bird card.
- Read status is kept on the server (/huddle-read) so it matches on every device; the server sends `hx`
  ({unread, fresh, last}) with each huddle in the Huddles feed."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v992.js'
dst = '_deploy/assets/index-DUcNPOLc-v993.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# 1. Huddle cards in the feed use the inbox card
patch('return(0,L.jsxs)(`div`,{className:`content-card feed-post-card`,style:{marginBottom:16},',
      'if(e.is_huddle)return(0,L.jsx)(_HC,{post:e,members:_fHm||[]});return(0,L.jsxs)(`div`,{className:`content-card feed-post-card`,style:{marginBottom:16},',
      'huddle card')
# 2. Huddle page: member row instead of the pill list
patch('c.is_huddle&&Array.isArray(e)&&e.length>0?(0,L.jsxs)(`div`,{style:{marginTop:0},children:[(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginBottom:6},children:`Huddle with:`}),',
      'c.is_huddle&&Array.isArray(e)&&e.length>0?(0,L.jsx)(_HxRow,{post:c,members:e}):c.is_huddle&&Array.isArray(e)&&e.length>0?(0,L.jsxs)(`div`,{style:{marginTop:0},children:[(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginBottom:6},children:`Huddle with:`}),',
      'huddle page member row')
# 3. Remember which open chats are huddles, and send read progress for them to the server
patch('if(!_un0&&_rp0)_cpRep[r]=_rp0;', 'if(!_un0&&_rp0)_cpRep[r]=_rp0;if(t&&t.is_huddle)_hxIds.add(r);', 'huddle ids')
patch('function _rdSet(p,t){try{const o=_rdGet(p);if(t&&(!o||t>o))localStorage.setItem(`pp_rd_`+p,t)}catch(e){}}',
      'function _rdSet(p,t){try{const o=_rdGet(p);if(t&&(!o||t>o))localStorage.setItem(`pp_rd_`+p,t)}catch(e){}_hxIds.has(p)&&_hxPost(p,t)}',
      'read sync')

c += r'''
var _hxIds=new Set(),_hxSent={},_hxT={};
function _hxPost(p,t){if(!t||(_hxSent[p]&&t<=_hxSent[p])||!localStorage.getItem(`auth_token`))return;clearTimeout(_hxT[p]);
 _hxT[p]=setTimeout(()=>{if(_hxSent[p]&&t<=_hxSent[p])return;_hxSent[p]=t;fetch(`${R}/huddle-read`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({post_id:p,at:t}),keepalive:!0}).catch(()=>{_hxSent[p]=null})},1200)}
function _hxCol(m){return m.role===`admin`?`#ffffff`:m.role===`mod`?`#c084fc`:Hn(m.browser_id,m.username)}
function _hxFace(m,sz){const b=Jn({username:m.username,browser_id:m.browser_id||null,is_admin:m.role===`admin`,is_mod:m.role===`mod`});
 if(b&&b.hat)return(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:sz+2,height:sz+2,objectFit:`contain`}});
 return(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,fontSize:sz,lineHeight:1},children:[(0,L.jsx)(`span`,{style:b&&b.f?{filter:b.f}:{},children:b&&b.e||`🐦`}),...(b&&b.s?_spEls(b.s,sz):[])]})}
function _hxAll(post,members){const own=(post.username||``).toLowerCase();
 return[{username:post.username,browser_id:post.browser_id||null,role:post.is_admin?`admin`:post.is_mod?`mod`:null,owner:!0},...members.filter(m=>m&&m.username&&m.username.toLowerCase()!==own)].filter(m=>m.username)}
function _hxDot(m,sz,lit,dim){const k=_hxCol(m),mx=p=>`color-mix(in srgb, ${k} ${p}%, transparent)`;
 return(0,L.jsxs)(`span`,{className:`hx-dot`+(lit?` lit`:``)+(dim?` dim`:``),style:{width:sz,height:sz,background:`color-mix(in srgb, ${k} ${lit?34:20}%, #1b1d24)`,border:`1.5px solid ${lit?k:mx(35)}`,boxShadow:lit?`0 0 0 2px #15171d, 0 0 12px ${mx(70)}`:`0 0 0 2px #15171d`},children:[_hxFace(m,Math.round(sz*.56)),m.owner?(0,L.jsx)(`span`,{className:`hx-crown`,children:`👑`}):null]},m.username)}
function _hxText(raw){try{const r=Mr(raw||``);let t=(r.text||``),ai=t.search(/\[ATTACH/),att=ai>=0||!!(r.attachments||r.attachment);if(ai>=0)t=t.slice(0,ai);t=t.replace(/\s+/g,` `).trim();if(t)return att?`📷 `+t:t;if(ai>=0)return/video/i.test(raw)?`🎬 Video`:`📷 Photo`;const a=r.attachments||r.attachment;const v=Array.isArray(a)?a[0]:a;return v&&v.type===`video`?`🎬 Video`:v?`📷 Photo`:``}catch(e){return String(raw||``).slice(0,140)}}
function _HC({post:e,members:mm}){const me=(Qn()?.username||``).toLowerCase(),hx=e.hx||null;_hxIds.add(e.id);
 let unread=hx?hx.unread||0:0,fresh=new Set((hx&&hx.fresh||[]).map(x=>String(x).toLowerCase()));
 const loc=_rdGet(e.id),caught=!!(hx&&hx.last&&loc&&loc>=hx.last.t&&unread);if(caught){unread=0;fresh=new Set()}
 (0,_.useEffect)(()=>{if(caught)_hxPost(e.id,loc)},[caught]);
 const others=_hxAll(e,mm).filter(m=>m.username.toLowerCase()!==me);
 others.sort((a,b)=>(fresh.has(b.username.toLowerCase())?1:0)-(fresh.has(a.username.toLowerCase())?1:0));
 const shown=others.slice(0,7),extra=others.length-shown.length;
 const last=hx&&hx.last,lu=last&&last.u,sys=lu===`__system__`,lm=lu&&lu.toLowerCase()===me;
 const lmem=lu&&!sys&&!lm?_hxAll(e,mm).find(m=>m.username.toLowerCase()===lu.toLowerCase())||{username:lu}:null;
 const prev=last?(0,L.jsxs)(`div`,{className:`hc-last`,children:[sys?null:(0,L.jsx)(`b`,{style:{color:lm?`#cbd5e1`:(()=>{const k=_hxCol(lmem);return k===`#ffffff`?`#e5e7eb`:k})()},children:lm?`You`:lu},`n`),sys?null:`: `,_hxText(last.c)]}):(0,L.jsx)(`div`,{className:`hc-last hc-none`,children:`No chirps yet — say hi 👋`});
 const when=Un(last&&last.t||e.last_activity||e.created_at).replace(` ago`,``);
 return(0,L.jsxs)(I,{to:`/post/${e.id}?chat=1&via=card`,className:`hc-card`+(unread?` hc-unread`:``),children:[
  (0,L.jsxs)(`div`,{className:`hc-top`,children:[(0,L.jsx)(`div`,{className:`hc-title`,children:e.title||`Huddle`}),(0,L.jsx)(`span`,{className:`hc-time`,children:when}),unread?(0,L.jsx)(`span`,{className:`hc-badge`,children:unread>99?`99+`:unread}):null]}),
  (0,L.jsxs)(`div`,{className:`hc-dots`,children:[...shown.map(m=>_hxDot(m,34,fresh.has(m.username.toLowerCase()),unread&&!fresh.has(m.username.toLowerCase()))),extra>0?(0,L.jsx)(`span`,{className:`hx-more`,children:`+${extra}`},`more`):null]}),
  prev]})}
function _HxRow({post,members}){const me=(Qn()?.username||``).toLowerCase(),all=_hxAll(post,members);
 const names=all.map(m=>m.username.toLowerCase()===me?`You`:m.username),txt=names.length<=2?names.join(` and `):`${names[0]} and ${names.length-1} others`;
 return(0,L.jsxs)(`button`,{type:`button`,className:`hx-row`,onClick:ev=>{ev.stopPropagation();_hxSheet(post,members)},children:[
  (0,L.jsx)(`span`,{className:`hc-dots`,children:all.slice(0,5).map(m=>_hxDot(m,30,!1,!1))}),
  (0,L.jsxs)(`span`,{className:`hx-rt`,children:[(0,L.jsx)(`span`,{className:`hx-cnt`,children:`${all.length} birds`}),(0,L.jsx)(`span`,{className:`hx-names`,children:txt})]}),(0,L.jsx)(`span`,{className:`hx-chev`,children:`›`})]})}
function _hxSheet(post,members){const me=(Qn()?.username||``).toLowerCase(),all=_hxAll(post,members);const host=document.createElement(`div`);document.body.append(host);const root=(0,g.createRoot)(host);
 const close=()=>{host.querySelector(`.hx-sheet`)?.classList.remove(`in`);setTimeout(()=>{root.unmount();host.remove()},200);removeEventListener(`popstate`,close)};addEventListener(`popstate`,close);
 root.render((0,L.jsxs)(`div`,{className:`hx-back`,onClick:close,children:[(0,L.jsxs)(`div`,{className:`hx-sheet`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(`div`,{className:`bc-grab`}),
  (0,L.jsxs)(`div`,{className:`hx-sh`,children:[`Members`,(0,L.jsx)(`span`,{children:all.length})]}),
  (0,L.jsx)(`div`,{className:`hx-list`,children:all.map(m=>{const k=_hxCol(m),mine=m.username.toLowerCase()===me;return(0,L.jsxs)(`div`,{className:`hx-item`,"data-gpb":mine?void 0:m.username,style:{background:`color-mix(in srgb, ${k} 7%, #15171d)`,border:`1px solid color-mix(in srgb, ${k} 22%, transparent)`},children:[
   _hxDot({...m,owner:!1},40,!1,!1),(0,L.jsx)(`span`,{className:`hx-nm`,style:{color:k===`#ffffff`?`#f1f5f9`:k},children:m.username}),
   m.owner?(0,L.jsx)(`span`,{className:`hx-tag`,children:`👑 Owner`}):null,mine?(0,L.jsx)(`span`,{className:`hx-tag`,children:`You`}):null]},m.username)})})]})]}));
 requestAnimationFrame(()=>requestAnimationFrame(()=>host.querySelector(`.hx-sheet`)?.classList.add(`in`)))}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.hc-card{display:flex;flex-direction:column;gap:10px;margin:0 0 12px;padding:14px 16px;border-radius:20px;text-decoration:none;color:inherit;background:#171a21;border:1px solid #262a35;transition:background .2s,border-color .2s,box-shadow .2s;-webkit-tap-highlight-color:transparent}
.hc-card:active{background:#1b1f28}
.hc-card.hc-unread{background:color-mix(in srgb, #c084fc 13%, #15171d);border-color:color-mix(in srgb, #c084fc 70%, transparent);box-shadow:0 0 0 1px color-mix(in srgb, #c084fc 28%, transparent),0 0 18px color-mix(in srgb, #c084fc 32%, transparent)}
.hc-top{display:flex;align-items:center;gap:8px;min-width:0}
.hc-title{flex:1;min-width:0;font-size:16px;font-weight:600;color:#cbd5e1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left}
.hc-unread .hc-title{font-weight:800;color:#f8fafc}
.hc-time{flex-shrink:0;font-size:12px;color:#64748b;font-weight:600}
.hc-unread .hc-time{color:#d8b4fe}
.hc-badge{flex-shrink:0;min-width:22px;height:22px;padding:0 7px;border-radius:999px;background:#c084fc;color:#14081d;font-size:12px;font-weight:800;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box}
.hc-dots{display:flex;align-items:center;padding-left:6px}
.hx-dot{position:relative;flex-shrink:0;margin-left:-6px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;transition:opacity .2s}
.hx-dot.dim{opacity:.4}
.hx-crown{position:absolute;top:-9px;right:-4px;font-size:12px;line-height:1;filter:drop-shadow(0 1px 1px rgba(0,0,0,.6))}
.hx-more{margin-left:6px;font-size:12px;font-weight:700;color:#94a3b8}
.hc-last{font-size:13.5px;line-height:1.4;color:#8b98a9;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left}
.hc-last b{font-weight:700}
.hc-unread .hc-last{color:#e2e8f0}
.hc-none{font-style:italic;color:#64748b}
.hx-row{display:flex;align-items:center;gap:12px;width:100%;margin-top:4px;padding:8px 10px 8px 4px;border:0;border-radius:14px;background:none;font-family:inherit;cursor:pointer;text-align:left;-webkit-tap-highlight-color:transparent}
.hx-row:active{background:rgba(148,163,184,.08)}
.hx-rt{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px}
.hx-cnt{font-size:13px;font-weight:700;color:#e2e8f0}
.hx-names{font-size:12px;line-height:1.35;color:#8b98a9;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow-wrap:anywhere}
.hx-chev{font-size:22px;color:#64748b;line-height:1}
.hx-back{position:fixed;inset:0;z-index:1500;background:rgba(0,0,0,.6);display:flex;align-items:flex-end;justify-content:center}
.hx-sheet{width:100%;max-width:480px;max-height:78vh;overflow:auto;background:#161920;border-radius:18px 18px 0 0;padding:0 14px calc(24px + env(safe-area-inset-bottom));box-shadow:0 -8px 40px rgba(0,0,0,.4);transform:translateY(100%);transition:transform .22s cubic-bezier(.3,.7,.2,1)}
.hx-sheet.in{transform:none}
.hx-sh{display:flex;align-items:center;gap:8px;padding:4px 4px 12px;font-size:16px;font-weight:800;color:#f1f5f9}
.hx-sh span{font-size:12px;font-weight:700;color:#94a3b8;background:rgba(148,163,184,.12);border-radius:999px;padding:2px 8px}
.hx-list{display:flex;flex-direction:column;gap:7px}
.hx-item{display:flex;align-items:center;gap:12px;padding:8px 14px 8px 14px;border-radius:20px;cursor:pointer}
.hx-item .hx-dot{margin-left:0}
.hx-nm{flex:1;min-width:0;font-size:14.5px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hx-tag{flex-shrink:0;font-size:11.5px;font-weight:700;color:#cbd5e1;background:rgba(148,163,184,.12);border-radius:999px;padding:3px 9px}
@media (prefers-reduced-motion: reduce){.hx-sheet{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
