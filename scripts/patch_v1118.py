#!/usr/bin/env python3
"""Patch v1117 -> v1118: worms you give, and a Flaps tab on profiles.
- Posts (feed cards and the post page) get a worm button next to flap / chirp / share: each tap gives the author one
  more worm (as many as you like). Our own worm icon; rose once you've given one.
- Chirps: the 🪱 reaction gives a worm to whoever wrote the chirp (not the post's author), shown as a worm pill that
  counts up; tapping the pill gives another.
- Profiles (See Posts): a Posts | Flaps switch. Flaps lists the posts that person flapped, newest first (public;
  huddles never show). Worm counts on profiles are now worms received (server side)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1117.js'
dst = '_deploy/assets/index-DUcNPOLc-v1118.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

WORM = ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
        '<path d=\\"M3 16.5c1.8-3.4 4.2-3.4 6 0s4.2 3.4 6 0 3.6-3.4 5.2-1.2\\"/><circle cx=\\"20.5\\" cy=\\"13.2\\" r=\\"1.7\\"/></svg>')
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', '"WORM": "' + WORM + '", "SHARE": "<svg class=\\"ri ri-arrow\\"', 'worm icon')

# --- the worm store (counts per post/chirp, loaded in batches) and the worm button ---
store = r'''const _ppWorm=(()=>{const cnt=new Map(),mine=new Map(),subs=new Map(),q=new Set(),pend=new Map();let t=null;
 const key=(k,id)=>k+`:`+id,emit=K=>(subs.get(K)||[]).forEach(f=>{try{f()}catch(e){}});
 const flush=()=>{t=null;const ks=[...q];q.clear();const posts=ks.filter(x=>x[0]===`p`).map(x=>x.slice(2)),comments=ks.filter(x=>x[0]===`c`).map(x=>x.slice(2));
  fetch(`${R}/worm-counts`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({posts,comments})}).then(r=>r.ok?r.json():null).then(d=>{if(!d)return;
   for(const[k,ids,o]of[[`p`,posts,d.posts||{}],[`c`,comments,d.comments||{}]])for(const id of ids){const K=key(k,id),v=o[id]||{n:0,m:0};if(pend.get(K))continue;cnt.set(K,v.n);mine.set(K,v.m);emit(K)}}).catch(()=>{})};
 const want=(k,id)=>{const K=key(k,id);if(cnt.has(K)||q.has(K))return;q.add(K);if(!t)t=setTimeout(flush,60)};
 const give=(k,id)=>{if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return!1}const K=key(k,id);
  cnt.set(K,(cnt.get(K)||0)+1);mine.set(K,(mine.get(K)||0)+1);pend.set(K,(pend.get(K)||0)+1);emit(K);
  fetch(`${R}/give-worm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify(k===`p`?{post_id:id}:{comment_id:id})}).then(r=>r.json().then(d=>({ok:r.ok,d}))).then(({ok,d})=>{
   const left=(pend.get(K)||1)-1;pend.set(K,left);
   if(ok&&d&&d.worms!=null){if(!left){cnt.set(K,d.worms);mine.set(K,d.mine)}}else{cnt.set(K,Math.max(0,(cnt.get(K)||1)-1));mine.set(K,Math.max(0,(mine.get(K)||1)-1));try{_hxToast(d&&d.error||`Could not give the worm`)}catch(e){}}emit(K)}).catch(()=>{pend.set(K,Math.max(0,(pend.get(K)||1)-1))});return!0};
 const sub=(K,f)=>{let s=subs.get(K);if(!s)subs.set(K,s=new Set());s.add(f);return()=>s.delete(f)};
 return{key,want,give,sub,n:K=>cnt.get(K)||0,m:K=>mine.get(K)||0}})();
function _WormPill({k,id,chirp,solo}){const K=_ppWorm.key(k,id),[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{_ppWorm.want(k,id);return _ppWorm.sub(K,()=>f(x=>x+1))},[K]);
 const n=_ppWorm.n(K),m=_ppWorm.m(K);if(chirp&&!n)return null;
 const b=(0,L.jsxs)(`button`,{type:`button`,className:(chirp?`chat-reaction-pill pp-worm-pill`:`feed-post-action-pill pp-worm-pill`)+(m?` mine`:``),title:`Give a worm`,"aria-label":`Give a worm (${n} so far)`,
  onClick:ev=>{ev.preventDefault();ev.stopPropagation();const el=ev.currentTarget;if(_ppWorm.give(k,id)){el.classList.remove(`pop`);void el.offsetWidth;el.classList.add(`pop`)}},
  children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:n})]},`worm`);
 return solo?(0,L.jsx)(`div`,{className:`chat-reactions rx-fit`,children:b}):b}
function _PFTabs({u,on}){const q=encodeURIComponent(u);return(0,L.jsxs)(`div`,{className:`pf-tabs`,children:[
 (0,L.jsx)(I,{to:`/?user=${q}`,replace:!0,className:`pf-tab`+(on?``:` on`),children:`Posts`}),
 (0,L.jsxs)(I,{to:`/?user=${q}&flaps=1`,replace:!0,className:`pf-tab`+(on?` on`:``),children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),`Flaps`]})]})}
'''
patch("function _ppFlapAnim(root){", store + "function _ppFlapAnim(root){", 'worm store, worm button, profile tabs')

# --- feed card: worm button before Share (not on huddles, feedback or bot posts) ---
patch("!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:h,",
      "!(e.is_huddle||e.community_id===`feedback`)&&!String(e.browser_id||``).startsWith(`bot-`)&&(0,L.jsx)(_WormPill,{k:`p`,id:e.id}),!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:h,", 'feed card worm')
# --- post page: worm button after flap ---
patch("children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:re.score})]}),",
      "children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:re.score})]}),!c?.is_huddle&&c&&!String(c.browser_id||``).startsWith(`bot-`)&&(0,L.jsx)(_WormPill,{k:`p`,id:c.id}),", 'post page worm')

# --- chirps: 🪱 gives a worm to the chirp's author; the worm pill replaces the 🪱 reaction pill ---
patch("async function ne(e,t){if(!localStorage.getItem(`auth_token`)){", "async function ne(e,t){if(t===`🪱`){_ppWorm.give(`c`,e);return}if(!localStorage.getItem(`auth_token`)){", 'worm reaction gives a worm')
patch("E=l[e.id]||{},ee=Object.entries(E);", "E=l[e.id]||{},ee=Object.entries(E).filter(([q])=>q!==`🪱`);", 'old worm reactions hidden')
patch("ee.length>0&&(0,L.jsxs)(`div`,{className:`chat-reactions rx-fit`,ref:el=>{el&&_rxFit(el)},children:[..._rxSort(ee)",
      "ee.length>0?(0,L.jsxs)(`div`,{className:`chat-reactions rx-fit`,ref:el=>{el&&_rxFit(el)},children:[(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1}),..._rxSort(ee)", 'worm pill in reactions')
patch("_setRxW(`all`)}},`__more`)]})", "_setRxW(`all`)}},`__more`)]}):(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,solo:1})", 'worm pill on its own')

# --- profiles: Posts | Flaps ---
patch("window.location.href=_hu;}}),(0,L.jsxs)(`main`,{className:`home-feed`",
      "window.location.href=_hu;}}),p&&!(u===`feedback`||u===`huddles`)&&(0,L.jsx)(_PFTabs,{u:l.get(`user`)||p,on:!!l.get(`flaps`)}),(0,L.jsxs)(`main`,{className:`home-feed`", 'profile tabs')
patch("if(p)turl+=`&username=${encodeURIComponent(l.get(`user`)||p)}`", "if(p)turl+=l.get(`flaps`)?`&flapped_by=${encodeURIComponent(l.get(`user`)||p)}`:`&username=${encodeURIComponent(l.get(`user`)||p)}`", 'flaps list')
patch("},[u,d,f,p,_cs])", "},[u,d,f,p,_cs,l.get(`flaps`)])", 'reload on switch')
patch("if(p)_url+=`&username=${encodeURIComponent(l.get(`user`)||p)}`", "if(p)_url+=l.get(`flaps`)?`&flapped_by=${encodeURIComponent(l.get(`user`)||p)}`:`&username=${encodeURIComponent(l.get(`user`)||p)}`", 'older flaps')

css = ("body .pp-worm-pill .pp-ic .ri{width:15px;height:15px;stroke-width:2.1;display:block}"
       "body .pp-worm-pill.mine{border-color:#fb7185!important;background:rgba(251,113,133,.14)!important;color:#fecdd3}body .pp-worm-pill.mine .pp-ic{color:#fb7185}"
       "body .pp-worm-pill.pop .pp-ic .ri{animation:ppWormPop .45s cubic-bezier(.3,1.6,.5,1)}@keyframes ppWormPop{0%{transform:scale(1)}40%{transform:scale(1.45) rotate(-12deg)}100%{transform:scale(1)}}"
       "body .chat-reaction-pill.pp-worm-pill{display:inline-flex;align-items:center;gap:3px}"
       "body .pf-tabs{display:flex;gap:8px;max-width:480px;margin:2px auto 10px;padding:0 14px;box-sizing:border-box}"
       "body .pf-tab{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:5px;height:34px;border-radius:999px;border:1px solid rgba(192,132,252,.3);background:rgba(192,132,252,.06);color:#c084fc;font-size:13px;font-weight:700;text-decoration:none}"
       "body .pf-tab.on{background:#c084fc;border-color:#c084fc;color:#14081d}body .pf-tab .pp-ic .ri{width:15px;height:15px;stroke-width:2.2;display:block}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
