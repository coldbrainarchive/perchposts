#!/usr/bin/env python3
"""Patch v1295 -> v1296: Share -> Send to a huddle.
- Signed in, every Share button (feed card, post page, post scroller) opens a minimal sheet: your huddles (bird
  circles, pick one or more), a chirp-style message box + round send button in your colour, and two pills:
  Copy link / More... (the iPhone share sheet, as before). Signed out: straight to the iPhone share sheet.
- Sending posts a chirp in each picked huddle: optional message + [ATTACH:{type:"post",id}].
- In chirps, a {type:"post"} attachment renders as a post card (site/bird, title, photo, live flap + chirp counts,
  "join in" when it has chirps) that opens the public post. Data from /share-card (public posts only)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1295.js'
dst = '_deploy/assets/index-DUcNPOLc-v1296.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# shared post card inside chirps
patch("function Fr({attachment:e,postId:o,maxH:_mh=480}){if(!e)return null;",
      "function Fr({attachment:e,postId:o,maxH:_mh=480}){if(!e)return null;if(e.type===`post`&&e.id)return(0,L.jsx)(_PPShareCard,{id:e.id});", 'post card in chirps')
# feed card share
patch("async function h(t){t.preventDefault(),t.stopPropagation();let n=`${window.location.origin}/post/${e.id}`;try{",
      "async function h(t){t.preventDefault(),t.stopPropagation();if(window._ppShare&&window._ppShare(e.id))return;let n=`${window.location.origin}/post/${e.id}`;try{", 'feed card share')
# post page share
patch("!c?.is_huddle&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async e=>{e.preventDefault();let t=`${window.location.origin}/post/${c.id}`;try{",
      "!c?.is_huddle&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async e=>{e.preventDefault();if(window._ppShare&&window._ppShare(c.id))return;let t=`${window.location.origin}/post/${c.id}`;try{", 'post page share')
# scroller share
patch("sh.onclick=async e=>{e.stopPropagation();const u=`${location.origin}/post/${d.post}`;",
      "sh.onclick=async e=>{e.stopPropagation();if(window._ppShare&&window._ppShare(d.post))return;const u=`${location.origin}/post/${d.post}`;", 'scroller share')
CSS = ("body .ps-ov{position:fixed;inset:0;z-index:9700;background:rgba(0,0,0,.55);display:flex;align-items:flex-end;justify-content:center;opacity:0;transition:opacity .2s}body .ps-ov.in{opacity:1}"
 "body .ps-sheet{width:100%;max-width:480px;background:#161920;border-radius:20px 20px 0 0;padding:8px 20px calc(24px + env(safe-area-inset-bottom));transform:translateY(100%);transition:transform .24s cubic-bezier(.22,.8,.24,1);box-sizing:border-box}body .ps-ov.in .ps-sheet{transform:none}"
 "body .ps-grab{width:36px;height:4px;border-radius:2px;background:#33363f;margin:0 auto 16px}body .ps-lbl{font-size:13px;font-weight:600;color:#64748b;margin:0 0 12px}"
 "body .ps-hds{display:flex;gap:16px;overflow-x:auto;padding:5px 5px 2px;margin:-5px -5px 0;scrollbar-width:none}body .ps-hds::-webkit-scrollbar{display:none}"
 "body .ps-hd{background:none;border:0;padding:0;display:flex;flex-direction:column;align-items:center;gap:6px;width:58px;flex-shrink:0;font:inherit;color:#94a3b8;cursor:pointer;-webkit-tap-highlight-color:transparent}"
 "body .ps-av{position:relative;width:50px;height:50px;border-radius:50%;background:#1f222b;transition:box-shadow .15s;display:flex;align-items:center;justify-content:center}body .ps-hd.on .ps-av{box-shadow:0 0 0 2px #161920,0 0 0 4px #c084fc}body .ps-hd.on .ps-nm{color:#f1f5f9}"
 "body .ps-b{position:absolute;display:inline-flex;line-height:1}body .ps-b1{left:3px;top:4px}body .ps-b2{right:2px;bottom:3px;transform:scaleX(-1)}body .ps-solo{display:inline-flex;line-height:1}body .ps-av .ps-hi{width:22px;height:22px;color:#94a3b8}"
 "body .ps-nm{font-size:11px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:58px}body .ps-empty{font-size:13px;color:#64748b;padding:6px 0 4px}"
 "body .ps-msg{display:flex;align-items:center;gap:8px;margin-top:16px}body .ps-bub{flex:1;height:44px;display:flex;align-items:center;background:#0d0f14;border:1px solid rgba(255,255,255,.07);border-radius:28px;padding:0 16px}"
 "body .ps-bub input{flex:1;min-width:0;border:0;background:none;color:#e2e8f0;font:inherit;font-size:16px;outline:none;-webkit-appearance:none;appearance:none}body .ps-bub input::-webkit-search-cancel-button{display:none;-webkit-appearance:none}"
 "body .ps-send{width:40px;height:40px;border-radius:999px;border:0;background:var(--me,#c084fc);color:#14081d;display:flex;align-items:center;justify-content:center;flex-shrink:0;cursor:pointer}body .ps-send:disabled{opacity:.6}body .ps-send svg{width:18px;height:18px}"
 "body .ps-sep{height:1px;background:#23262e;margin:16px 0 14px}body .ps-lns{display:flex;gap:10px}"
 "body .ps-ln{display:flex;align-items:center;justify-content:center;gap:8px;flex:1;height:40px;border-radius:999px;border:1px solid #323b48;background:#1d242d;color:#e5edf6;font:inherit;font-size:14px;font-weight:700;letter-spacing:.02em;padding:0 14px;cursor:pointer}body .ps-ln svg{width:16px;height:16px;flex-shrink:0}"
 "body .ps-note{text-align:center;font-size:13px;font-weight:700;color:#e9d5ff;margin-top:12px;min-height:18px}"
 "body .psc{display:flex;gap:10px;align-items:stretch;text-decoration:none;color:inherit;background:#1a1d27;border:1px solid rgba(148,163,184,.15);border-radius:12px;padding:10px;min-height:64px;margin-bottom:2px;cursor:pointer}"
 "body .psc-t{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}body .psc-s{font-size:10px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#c084fc}"
 "body .psc-h{font-size:14px;font-weight:700;color:#f1f5f9;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}"
 "body .psc-c{display:flex;align-items:center;gap:10px;margin-top:auto;font-size:12px;font-weight:700;color:#94a3b8}body .psc-c span{display:inline-flex;align-items:center;gap:4px}body .psc-c svg{width:13px;height:13px}body .psc-j{color:#c084fc}"
 "body .psc-i{width:64px;height:64px;border-radius:8px;object-fit:cover;flex-shrink:0;background:#0d0f14}body .psc.gone{color:#64748b;font-size:13px;align-items:center;justify-content:center;min-height:44px}")
patch("body .lb-ic{", CSS + "body .lb-ic{", 'css')
LINK = '<svg viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"><path d=\\"M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71\\"/><path d=\\"M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71\\"/></svg>'
UP = '<svg viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2.6\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"><path d=\\"M12 19V5M5 12l7-7 7 7\\"/></svg>'
c += r"""
function _ppFace(name,z){try{const l=String(name||``).toLowerCase(),b=Jn({username:name,browser_id:null,is_admin:typeof _adminUsers!==`undefined`&&_adminUsers.has(l),is_mod:typeof _modUsers!==`undefined`&&_modUsers.has(l)})||{};
 return b.hat?(0,L.jsx)(_PB,{n:`admin`,c:`A`,z,k:`t`,fb:(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:z,height:z,objectFit:`contain`}})}):(0,L.jsx)(`span`,{style:b.f?{filter:b.f,display:`inline-flex`}:{display:`inline-flex`},children:b.e?_ppB(b,z,`t`):`🐦`})}catch(e){return null}}
const _psCache=new Map();
function _PPShareCard({id}){const[d,setD]=(0,_.useState)(()=>_psCache.get(id)||null);
 (0,_.useEffect)(()=>{let dead=!1;fetch(`${R}/share-card?id=${encodeURIComponent(id)}`,{headers:er()}).then(r=>r.ok?r.json():{gone:!0}).then(x=>{_psCache.set(id,x);dead||setD(x)}).catch(()=>{});return()=>{dead=!0}},[id]);
 const go=ev=>{ev.preventDefault();ev.stopPropagation();try{history.pushState({},``,`/post/${id}`);dispatchEvent(new PopStateEvent(`popstate`,{state:{}}))}catch(e){location.href=`/post/${id}`}};
 if(!d)return(0,L.jsx)(`div`,{className:`psc`,onClick:ev=>ev.stopPropagation()});
 if(d.gone)return(0,L.jsx)(`div`,{className:`psc gone`,onClick:ev=>ev.stopPropagation(),children:`This post isn't available`});
 return(0,L.jsxs)(`a`,{className:`psc`,href:`/post/${id}`,onClick:go,children:[(0,L.jsxs)(`div`,{className:`psc-t`,children:[(0,L.jsx)(`div`,{className:`psc-s`,children:d.site||d.by||`perchposts`}),(0,L.jsx)(`div`,{className:`psc-h`,children:d.title||d.text||`Post`}),
   (0,L.jsxs)(`div`,{className:`psc-c`,children:[(0,L.jsxs)(`span`,{children:[(0,L.jsx)(`span`,{dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),d.flaps]}),(0,L.jsxs)(`span`,{children:[(0,L.jsx)(`span`,{dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}),d.chirps]}),d.chirps>0?(0,L.jsx)(`span`,{className:`psc-j`,children:`join in`}):null]})]}),
  d.image?(0,L.jsx)(`img`,{className:`psc-i`,src:d.image,alt:``,loading:`lazy`,onError:ev=>{ev.currentTarget.style.display=`none`}}):null]})}
function _ShareSheet({id,close}){const[hs,setHs]=(0,_.useState)(null),[sel,setSel]=(0,_.useState)([]),[msg,setMsg]=(0,_.useState)(``),[busy,setBusy]=(0,_.useState)(!1),[note,setNote]=(0,_.useState)(``),[inn,setIn]=(0,_.useState)(!1);
 const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase(),url=`${location.origin}/post/${id}`;
 (0,_.useEffect)(()=>{requestAnimationFrame(()=>setIn(!0));fetch(`${R}/my-huddles`,{headers:er()}).then(r=>r.ok?r.json():{huddles:[]}).then(x=>setHs(x.huddles||[])).catch(()=>setHs([]));const k=ev=>{ev.key===`Escape`&&bye()};addEventListener(`keydown`,k);return()=>removeEventListener(`keydown`,k)},[]);
 const bye=()=>{setIn(!1);setTimeout(close,240)};const done=t=>{setNote(t);setTimeout(bye,850)};
 const copy=async()=>{try{await navigator.clipboard.writeText(url);done(`Link copied`)}catch(e){setNote(`Couldn't copy the link`)}};
 const more=async()=>{try{if(navigator.share){await navigator.share({url});bye()}else{await navigator.clipboard.writeText(url);done(`Link copied`)}}catch(e){}};
 const pick=h=>setSel(s=>s.includes(h)?s.filter(x=>x!==h):[...s,h]);
 const send=async()=>{if(!sel.length||busy)return;setBusy(!0);setNote(``);let ok=0,err=``;const att=`\n\n[ATTACH:`+JSON.stringify({type:`post`,id})+`]`;
  for(const h of sel){try{const r=await fetch(`${R}/add-comment`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({content:msg.trim()+att,post_id:h,parent_comment_id:null,browser_id:Gn()})});if(r.ok)ok++;else{const j=await r.json().catch(()=>({}));err=j.error||`Couldn't send`}}catch(e){err=`Couldn't send`}}
  setBusy(!1);if(ok){const one=sel.length===1&&(hs||[]).find(x=>x.id===sel[0]);done(`Sent to ${one?one.title:ok+` huddles`}`)}else setNote(err===`Caged`?`You're Caged: you can only chirp in The Cage`:err)};
 const av=h=>{const o=(h.members||[]).filter(n=>n.toLowerCase()!==me).slice(0,2);return o.length===2?[(0,L.jsx)(`span`,{className:`ps-b ps-b1`,children:_ppFace(o[0],23)},`a`),(0,L.jsx)(`span`,{className:`ps-b ps-b2`,children:_ppFace(o[1],23)},`b`)]:o.length===1?(0,L.jsx)(`span`,{className:`ps-solo`,children:_ppFace(o[0],32)}):(0,L.jsx)(`span`,{className:`ps-hi`,dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}})};
 return(0,L.jsx)(`div`,{className:`ps-ov`+(inn?` in`:``),onClick:bye,children:(0,L.jsxs)(`div`,{className:`ps-sheet`,role:`dialog`,"aria-label":`Share`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(`div`,{className:`ps-grab`}),
  (0,L.jsx)(`div`,{className:`ps-lbl`,children:`Send to a huddle`}),
  hs===null?(0,L.jsx)(`div`,{className:`ps-empty`,children:`Loading…`}):hs.length===0?(0,L.jsx)(`div`,{className:`ps-empty`,children:`You're not in any huddles yet.`}):
  (0,L.jsx)(`div`,{className:`ps-hds`,children:hs.map(h=>(0,L.jsxs)(`button`,{type:`button`,className:`ps-hd`+(sel.includes(h.id)?` on`:``),onClick:()=>pick(h.id),"aria-pressed":sel.includes(h.id),children:[(0,L.jsx)(`span`,{className:`ps-av`,children:av(h)}),(0,L.jsx)(`span`,{className:`ps-nm`,children:h.title})]},h.id))}),
  sel.length?(0,L.jsxs)(`div`,{className:`ps-msg`,children:[(0,L.jsx)(`div`,{className:`ps-bub`,children:(0,L.jsx)(`input`,{type:`search`,name:`search_ps_msg`,autoComplete:`off`,enterKeyHint:`send`,placeholder:`Add a message…`,value:msg,maxLength:1000,onChange:ev=>setMsg(ev.target.value),onKeyDown:ev=>{if(ev.key===`Enter`){ev.preventDefault();send()}}})}),
   (0,L.jsx)(`button`,{type:`button`,className:`ps-send`,disabled:busy,"aria-label":sel.length>1?`Send to ${sel.length} huddles`:`Send`,onClick:send,dangerouslySetInnerHTML:{__html:`""" + UP + r"""`}})]}):null,
  (0,L.jsx)(`div`,{className:`ps-sep`}),
  (0,L.jsxs)(`div`,{className:`ps-lns`,children:[(0,L.jsxs)(`button`,{type:`button`,className:`ps-ln`,onClick:copy,children:[(0,L.jsx)(`span`,{style:{display:`inline-flex`},dangerouslySetInnerHTML:{__html:`""" + LINK + r"""`}}),`Copy link`]}),(0,L.jsxs)(`button`,{type:`button`,className:`ps-ln`,onClick:more,children:[(0,L.jsx)(`span`,{style:{display:`inline-flex`},dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),`More…`]})]}),
  note?(0,L.jsx)(`div`,{className:`ps-note`,role:`status`,children:note}):null]})})}
window._ppShare=id=>{try{if(!id||!localStorage.getItem(`auth_token`))return!1;const host=document.createElement(`div`);document.body.appendChild(host);const r=(0,g.createRoot)(host);
 try{const me=localStorage.getItem(`_myUsername`);if(me)host.style.setProperty(`--me`,Hn(Gn(),me))}catch(e){}
 r.render((0,L.jsx)(_ShareSheet,{id,close:()=>{setTimeout(()=>{try{r.unmount()}catch(e){}host.remove()},0)}}));return!0}catch(e){return!1}};
"""
patch("t=t.replace(/\\s+/g,` `).trim();if(t)return att?`📷 `+t:t;", "t=t.replace(/\\s+/g,` `).trim();if(r.attachment&&r.attachment.type===`post`)return t||`Shared a post`;if(t)return att?`📷 `+t:t;", 'huddle list preview')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
