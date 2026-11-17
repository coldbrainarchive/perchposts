#!/usr/bin/env python3
"""Patch v1118 -> v1119: one bird for everything.
- The bird number on posts counts the people who responded in any way (flapped, reacted or gave worms), each once.
  It's purple once you've done any of those. Tap = flap / un-flap, as before.
- Press and hold the bird: a picker with quick emoji, "+" for any emoji, and a worm row (- / + / Give).
- Chirps: the worm in the reaction bar opens the same worm picker (choose how many). The separate worm button is gone.
- Post page: a small reactions pill next to the bird, and "Reactions" in the chirp preview's menu, show who did what."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1118.js'
dst = '_deploy/assets/index-DUcNPOLc-v1119.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

SMILE = ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
         '<circle cx=\\"12\\" cy=\\"12\\" r=\\"8.5\\"/><path d=\\"M8.5 14.5c.9 1.3 2.1 2 3.5 2s2.6-.7 3.5-2\\"/><path d=\\"M9 9.8v.4M15 9.8v.4\\"/></svg>')
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', '"SMILE": "' + SMILE + '", "SHARE": "<svg class=\\"ri ri-arrow\\"', 'smile icon')
patch('const _PPE={"⏳":`HOURGLASS`,', 'const _PPE={"😀":`SMILE`,"⏳":`HOURGLASS`,', 'reactions label icon')

# ---------- shared per-post record + picker + reactions list ----------
js = r'''const _ppResp=(()=>{const m=new Map(),subs=new Map();
 const emit=id=>(subs.get(id)||[]).forEach(f=>{try{f()}catch(e){}});
 return{get:id=>m.get(id),set:(id,o)=>{m.set(id,{...(m.get(id)||{}),...o});emit(id)},sub:(id,f)=>{let s=subs.get(id);if(!s)subs.set(id,s=new Set());s.add(f);return()=>s.delete(f)}}})();
const _PPQ=[`❤️`,`😂`,`😮`,`😢`,`👍`,`🔥`];
function _ppReactPost(id,q){if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}
 const o=_ppResp.get(id)||{n:0,m:0};const same=o.emoji===q,em=same?null:q;
 _ppResp.set(id,{emoji:em,n:o.m?o.n:o.n+1,m:o.m||2});
 fetch(`${R}/react-post`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({post_id:id,emoji:q})}).then(r=>r.json()).then(d=>{if(d&&d.success)_ppResp.set(id,{n:d.score,m:d.myVote,emoji:d.emoji});else{_ppResp.set(id,o);try{_hxToast(d&&d.error||`Could not react`)}catch(e){}}}).catch(()=>_ppResp.set(id,o))}
// the picker: emoji (posts only) and a worm row; anchored to the button that opened it
function _ppPicker(anchor,kind,id){document.querySelector(`.pp-pick`)?.remove();
 if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}
 const pk=document.createElement(`div`);pk.className=`pp-pick`;pk.setAttribute(`role`,`dialog`);let cnt=1;
 const close=()=>{pk.remove();document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`scroll`,close,!0)};
 const out=e=>{if(!pk.contains(e.target))close()};
 if(kind===`p`){const row=document.createElement(`div`);row.className=`pp-pick-row`;const mine=(_ppResp.get(id)||{}).emoji;
  _PPQ.forEach(q=>{const b=document.createElement(`button`);b.type=`button`;b.className=`pp-pick-q`+(q===mine?` on`:``);b.textContent=q;b.setAttribute(`aria-label`,`React ${q}`);b.onclick=()=>{_ppReactPost(id,q);close()};row.append(b)});
  const pl=document.createElement(`button`);pl.type=`button`;pl.className=`pp-pick-q pp-pick-more`;pl.textContent=`+`;pl.setAttribute(`aria-label`,`More emoji`);pl.onclick=()=>{close();_rxPick(q=>_ppReactPost(id,q))};row.append(pl);pk.append(row)}
 const wr=document.createElement(`div`);wr.className=`pp-pick-worm`;
 wr.innerHTML=`<span class="pp-ic pp-worm">${_ppIco(`WORM`)}</span><span class="pp-pick-wl">Give worms</span><button type="button" class="pp-pick-st" aria-label="Fewer">−</button><b class="pp-pick-n">1</b><button type="button" class="pp-pick-st" aria-label="More">+</button><button type="button" class="pp-pick-give">Give</button>`;
 const [mn,pls]=wr.querySelectorAll(`.pp-pick-st`),nb=wr.querySelector(`.pp-pick-n`),gv=wr.querySelector(`.pp-pick-give`);
 const upd=()=>{nb.textContent=cnt;gv.textContent=cnt===1?`Give 1`:`Give ${cnt}`};upd();
 mn.onclick=()=>{cnt=Math.max(1,cnt-1);upd()};pls.onclick=()=>{cnt=Math.min(50,cnt+1);upd()};
 gv.onclick=()=>{_ppWorm.give(kind,id,cnt);close()};pk.append(wr);
 document.body.append(pk);const r=anchor.getBoundingClientRect(),w=pk.offsetWidth,h=pk.offsetHeight;
 pk.style.left=Math.max(8,Math.min(r.left,innerWidth-w-8))+`px`;pk.style.top=(r.top-h-8<8?r.bottom+8:r.top-h-8)+`px`;
 requestAnimationFrame(()=>pk.classList.add(`in`));setTimeout(()=>{document.addEventListener(`pointerdown`,out,!0);addEventListener(`scroll`,close,!0)},0)}
// press and hold the bird on a post: the picker (a plain tap still flaps)
;(()=>{try{let tm=null,fired=0,sx=0,sy=0;const bird=t=>{const b=t&&t.closest&&t.closest(`.feed-post-action-pill`);return b&&b.querySelector(`.pp-bird`)?b:null};
 const pid=b=>{const a=b.closest(`.feed-post-actions`)?.querySelector(`a[href*="/post/"]`);const m=(a?a.getAttribute(`href`):location.pathname).match(/\/post\/([^/?#]+)/);return m&&m[1]};
 addEventListener(`pointerdown`,e=>{const b=bird(e.target);if(!b)return;sx=e.clientX;sy=e.clientY;clearTimeout(tm);tm=setTimeout(()=>{const id=pid(b);if(!id)return;fired=Date.now();try{navigator.vibrate&&navigator.vibrate(10)}catch(_){}_ppPicker(b,`p`,id)},450)},!0);
 const stop=()=>clearTimeout(tm);addEventListener(`pointerup`,stop,!0);addEventListener(`pointercancel`,stop,!0);
 addEventListener(`pointermove`,e=>{if(Math.abs(e.clientX-sx)>10||Math.abs(e.clientY-sy)>10)stop()},!0);
 addEventListener(`contextmenu`,e=>{if(bird(e.target))e.preventDefault()},!0);
 addEventListener(`click`,e=>{if(fired&&Date.now()-fired<900&&bird(e.target)){fired=0;e.preventDefault();e.stopPropagation()}},!0)}catch(e){}})();
// who did what on a post
const _prxCache=new Map();
function _prxLoad(id){const p=fetch(`${R}/post-reactions?post_id=${encodeURIComponent(id)}`,{headers:er()}).then(r=>r.ok?r.json():{people:[]}).then(d=>d.people||[]).catch(()=>[]);_prxCache.set(id,p);return p}
function _usePrx(id){const[ppl,set]=(0,_.useState)(null);(0,_.useEffect)(()=>{let on=!0;(_prxCache.get(id)||_prxLoad(id)).then(v=>on&&set(v));const u=_ppResp.sub(id,()=>setTimeout(()=>_prxLoad(id).then(v=>on&&set(v)),400));return()=>{on=!1;u()}},[id]);return ppl}
function _PostReactions({id}){const ppl=_usePrx(id),[tab,setTab]=(0,_.useState)(`all`);
 if(!ppl)return(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`});
 if(!ppl.length)return(0,L.jsx)(`div`,{className:`cp-empty`,children:`No reactions yet`});
 const emo=new Map();ppl.forEach(p=>p.emoji&&emo.set(p.emoji,(emo.get(p.emoji)||0)+1));const nf=ppl.filter(p=>p.flap).length,nw=ppl.reduce((s,p)=>s+(p.worms||0),0);
 const ic=k=>(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}});
 const T=(k,ch)=>(0,L.jsx)(`button`,{type:`button`,className:`pr-tab`+(tab===k?` on`:``),onClick:ev=>{ev.stopPropagation();setTab(k)},children:ch},k);
 const show=ppl.filter(p=>tab===`all`||(tab===`flap`&&p.flap)||(tab===`worm`&&p.worms)||p.emoji===tab);
 return(0,L.jsxs)(`div`,{className:`pr-wrap`,onClick:ev=>ev.stopPropagation(),children:[
  (0,L.jsxs)(`div`,{className:`pr-tabs`,children:[T(`all`,`All ${ppl.length}`),nf?T(`flap`,[ic(`BIRD`),nf]):null,nw?T(`worm`,[ic(`WORM`),nw]):null,...[...emo].sort((a,b)=>b[1]-a[1]).map(([q,n])=>T(q,`${q} ${n}`))]}),
  (0,L.jsx)(`div`,{className:`pr-list`,children:show.map(p=>{const f=_rxFace(p.username,16),k=f.col;return(0,L.jsxs)(`div`,{className:`rx-row`,"data-gpb":p.username,style:{background:`color-mix(in srgb, ${k} 9%, #15171d)`,borderColor:`color-mix(in srgb, ${k} 22%, transparent)`},children:[
   (0,L.jsx)(`span`,{className:`rx-av`,style:{background:`color-mix(in srgb, ${k} 24%, #1b1d24)`,borderColor:`color-mix(in srgb, ${k} 40%, transparent)`},children:f.el}),
   (0,L.jsx)(`span`,{className:`rx-nm`,style:{color:k===`#ffffff`?`#e5e7eb`:k},children:p.username}),
   (0,L.jsxs)(`span`,{className:`pr-did`,children:[p.flap?ic(`BIRD`):null,p.emoji?(0,L.jsx)(`span`,{className:`pr-emo`,children:p.emoji}):null,p.worms?(0,L.jsxs)(`span`,{className:`pr-w`,children:[ic(`WORM`),p.worms]}):null]})]},p.username)})})]})}
// the small pill next to the bird on the post page: top emoji + worms; opens who did what
function _PostRespLine({id,pv,setCpm}){const ppl=_usePrx(id),[open,setOpen]=(0,_.useState)(!1);
 const emo=new Map();(ppl||[]).forEach(p=>p.emoji&&emo.set(p.emoji,(emo.get(p.emoji)||0)+1));const nw=(ppl||[]).reduce((s,p)=>s+(p.worms||0),0);
 const sheet=open?(0,L.jsx)(`div`,{className:`rx-ov`,onClick:ev=>{ev.stopPropagation();setOpen(!1)},children:(0,L.jsxs)(`div`,{className:`rx-sheet`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(`div`,{className:`rx-grab`}),(0,L.jsx)(_PostReactions,{id})]})}):null;
 if(!emo.size&&!nw)return sheet;
 return(0,L.jsxs)(L.Fragment,{children:[(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pr-line`,title:`See reactions`,onClick:ev=>{ev.preventDefault();ev.stopPropagation();if(pv){setCpm(`react`);setTimeout(()=>document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`}),50)}else setOpen(!0)},children:[
  emo.size?(0,L.jsx)(`span`,{className:`pr-emos`,children:[...emo].sort((a,b)=>b[1]-a[1]).slice(0,3).map(x=>x[0]).join(``)}):null,
  nw?(0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]}):null]}),sheet]})}
'''
patch("function _ppFlapAnim(root){", js + "function _ppFlapAnim(root){", 'record, picker, hold, reactions list')

# worms: give a chosen number; posts' answers update the bird
patch("const give=(k,id)=>{if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return!1}const K=key(k,id);\n  cnt.set(K,(cnt.get(K)||0)+1);mine.set(K,(mine.get(K)||0)+1);pend.set(K,(pend.get(K)||0)+1);emit(K);\n  fetch(`${R}/give-worm`,{method:`POST`,headers:{\"Content-Type\":`application/json`,...er()},body:JSON.stringify(k===`p`?{post_id:id}:{comment_id:id})})",
      "const give=(k,id,nn)=>{if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return!1}const K=key(k,id),N=Math.max(1,nn||1);\n  cnt.set(K,(cnt.get(K)||0)+N);mine.set(K,(mine.get(K)||0)+N);pend.set(K,(pend.get(K)||0)+1);emit(K);if(k===`p`){const o=_ppResp.get(id)||{n:0,m:0};_ppResp.set(id,{n:o.m?o.n:o.n+1,m:o.m||2})}\n  fetch(`${R}/give-worm`,{method:`POST`,headers:{\"Content-Type\":`application/json`,...er()},body:JSON.stringify(k===`p`?{post_id:id,count:N}:{comment_id:id,count:N})})", 'give a number of worms')
patch("if(ok&&d&&d.worms!=null){if(!left){cnt.set(K,d.worms);mine.set(K,d.mine)}}else{cnt.set(K,Math.max(0,(cnt.get(K)||1)-1));mine.set(K,Math.max(0,(mine.get(K)||1)-1));",
      "if(ok&&d&&d.worms!=null){if(!left){cnt.set(K,d.worms);mine.set(K,d.mine)}if(k===`p`&&d.score!=null)_ppResp.set(id,{n:d.score,m:d.myVote});try{_hxToast(N===1?`You gave a worm`:`You gave ${N} worms`)}catch(e){}}else{cnt.set(K,Math.max(0,(cnt.get(K)||N)-N));mine.set(K,Math.max(0,(mine.get(K)||N)-N));", 'worm answer')

# the bird number = people who responded (loaded for every list of posts)
i = c.index("async function Dr(e){"); j = c.index("var Or={World:", i)
c = c[:i] + ("async function Dr(e){if(!e.length)return{};e=e.slice(0,100);try{let n=await fetch(`${R}/post-responses?post_ids=${e.join(`,`)}`,{headers:er(),signal:AbortSignal.timeout(5e3)}).catch(()=>null);"
             "if(!n||!n.ok)n=await fetch(`${R}/post-responses?post_ids=${e.join(`,`)}`,{headers:er()});if(!n.ok)return{};let{posts:p}=await n.json(),i={};"
             "for(let id of e){const o=(p||{})[id]||{n:0,m:0};_ppResp.set(id,{n:o.n,m:o.m,emoji:o.emoji||null});i[id]={score:o.n,myVote:o.m,voteCount:o.n}}return i}catch{return{}}}") + c[j:]; print('OK: bird counts people')
patch("async function Tr(e,t){let n=er();return(await fetch(`${R}/vote-post`,{method:`POST`,headers:{\"Content-Type\":`application/json`,...n},body:JSON.stringify({post_id:e,browser_id:Gn(),value:t,username:localStorage.getItem(`mod_name`)||void 0})})).json()}",
      "async function Tr(e,t){let n=er();const d=await(await fetch(`${R}/vote-post`,{method:`POST`,headers:{\"Content-Type\":`application/json`,...n},body:JSON.stringify({post_id:e,browser_id:Gn(),value:t,username:localStorage.getItem(`mod_name`)||void 0})})).json();d&&d.success&&_ppResp.set(e,{n:d.score,m:d.myVote});return d}", 'flap updates the record')

# feed card: follow the shared record; purple once you've responded; no separate worm button
patch("function Ir({post:e,commentCount:t=0,score:n=0,myVote:r=0,onVote:i,showActivity:a=!1}){",
      "function Ir({post:e,commentCount:t=0,score:n=0,myVote:r=0,onVote:i,showActivity:a=!1}){const[,_rv]=(0,_.useState)(0);(0,_.useEffect)(()=>_ppResp.sub(e.id,()=>_rv(x=>x+1)),[e.id]);{const _o=_ppResp.get(e.id);if(_o&&_o.n!=null){n=_o.n;r=_o.m||0}}", 'card follows the record')
patch("style:r===1&&i?{borderColor:`#c084fc`", "style:r>=1&&i?{borderColor:`#c084fc`", 'card purple when responded')
patch("!(e.is_huddle||e.community_id===`feedback`)&&!String(e.browser_id||``).startsWith(`bot-`)&&(0,L.jsx)(_WormPill,{k:`p`,id:e.id}),", "", 'card worm button removed')

# post page: same, plus the reactions pill
patch("[oe,se]=(0,_.useState)(!1);(0,_.useEffect)(()=>{if(N)ret", "[oe,se]=(0,_.useState)(!1);(0,_.useEffect)(()=>_ppResp.sub(r,()=>{const o=_ppResp.get(r);o&&o.n!=null&&ie({score:o.n,myVote:o.m||0})}),[r]);(0,_.useEffect)(()=>{if(N)ret", 'post page follows the record')
patch("style:re.myVote===1?{borderColor:`#c084fc`", "style:re.myVote>=1?{borderColor:`#c084fc`", 'post page purple when responded')
patch("const _nv=re.myVote===1?0:1;const _os=re.score+_nv-(re.myVote||0);", "const _nv=re.myVote===1?0:1;const _os=_nv?re.score+(re.myVote?0:1):Math.max(0,re.score-1);", 'post page count guess')
patch("!c?.is_huddle&&c&&!String(c.browser_id||``).startsWith(`bot-`)&&(0,L.jsx)(_WormPill,{k:`p`,id:c.id}),", "!c?.is_huddle&&c&&(0,L.jsx)(_PostRespLine,{id:c.id,pv:_pv,setCpm:_setCpm}),", 'post page reactions pill')

# chirp preview menu: Reactions
patch("const _CPL={hl:`✨ Highlights`,top:`🔥 Top`,rep:`↩️ Most replied`,latest:`🕒 Latest`,media:`🖼️ Media`};", "const _CPL={hl:`✨ Highlights`,top:`🔥 Top`,rep:`↩️ Most replied`,latest:`🕒 Latest`,media:`🖼️ Media`,react:`😀 Reactions`};", 'menu option')
patch(":_cpm===`media`?_rev.filter(_x=>/\\[ATTACH/.test(_x.content||``)).slice(0,5):_rev.slice(0,5);", ":_cpm===`media`?_rev.filter(_x=>/\\[ATTACH/.test(_x.content||``)).slice(0,5):_cpm===`react`?[]:_rev.slice(0,5);", 'no chirps in Reactions')
patch("_pv&&_cpm!==`hl`&&!_nl&&de.length>0&&_out.push((0,L.jsx)(`div`,{className:`cp-empty`,children:_CPE[_cpm]},`cpe`));",
      "_pv&&_cpm===`react`?(!c?.is_huddle&&_out.push((0,L.jsx)(_PostReactions,{id:r},`prx`))):_pv&&_cpm!==`hl`&&!_nl&&de.length>0&&_out.push((0,L.jsx)(`div`,{className:`cp-empty`,children:_CPE[_cpm]},`cpe`));", 'Reactions list in the preview')

# chirps: the worm in the reaction bar opens the worm picker
patch("..._RXQ.map(q=>{const mine=(E[q]||[]).includes(me);\n   return(0,L.jsx)(`button`,{type:`button`,className:`rx-q${mine?` mine`:``}`,",
      "..._RXQ.map(q=>{const mine=(E[q]||[]).includes(me);\n   if(q===`🪱`)return(0,L.jsx)(`button`,{type:`button`,className:`rx-q rx-worm`,\"aria-label\":`Give worms`,onClick:ev=>{const b=ev.currentTarget.closest(`.rx-bar`)||ev.currentTarget;close();_ppPicker(b,`c`,id)},dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}},q);\n   return(0,L.jsx)(`button`,{type:`button`,className:`rx-q${mine?` mine`:``}`,", 'chirp worm picker')

patch("children:[de.length===0&&(0,L.jsx)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`center`,flex:1,minHeight:120},children:(0,L.jsx)(`p`,{style:{color:`rgba(148,163,184,0.3)`,fontSize:13,margin:0},children:`No chirps yet`})}),",
      "children:[de.length===0&&!(_pv&&_cpm===`react`)&&(0,L.jsx)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`center`,flex:1,minHeight:120},children:(0,L.jsx)(`p`,{style:{color:`rgba(148,163,184,0.3)`,fontSize:13,margin:0},children:`No chirps yet`})}),", 'no "No chirps yet" under Reactions')
css = ("body .feed-post-action-pill:has(.pp-bird){-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}"
       "body .pp-pick{position:fixed;z-index:9999;background:#1b1d24;border:1px solid #2e303a;border-radius:16px;padding:8px;box-shadow:0 12px 32px rgba(0,0,0,.5);display:flex;flex-direction:column;gap:8px;opacity:0;transform:translateY(4px) scale(.97);transition:opacity .14s,transform .14s}"
       "body .pp-pick.in{opacity:1;transform:none}body .pp-pick-row{display:flex;gap:2px}"
       "body .pp-pick-q{width:38px;height:38px;border-radius:999px;border:0;background:transparent;font-size:23px;line-height:1;cursor:pointer;padding:0;color:#cbd5e1;font-family:inherit}"
       "body .pp-pick-q.on{background:rgba(192,132,252,.22)}body .pp-pick-more{font-size:20px;font-weight:700;background:#262935}"
       "body .pp-pick-worm{display:flex;align-items:center;gap:8px;padding:6px 6px 2px 8px;border-top:1px solid #2a2d38;color:#fecdd3;font-size:13px;font-weight:700}"
       "body .pp-pick-worm .pp-ic{color:#fb7185}body .pp-pick-worm .pp-ic .ri{width:18px;height:18px;display:block}body .pp-pick-wl{flex:1;white-space:nowrap}"
       "body .pp-pick-st{width:28px;height:28px;border-radius:999px;border:1px solid #3a3d48;background:#22252e;color:#e2e8f0;font-size:16px;font-weight:700;cursor:pointer;padding:0;font-family:inherit}"
       "body .pp-pick-n{min-width:18px;text-align:center;color:#f1f5f9}"
       "body .pp-pick-give{height:30px;padding:0 12px;border-radius:999px;border:0;background:#fb7185;color:#1a0508;font-weight:800;font-size:13px;cursor:pointer;font-family:inherit}"
       "body .rx-q.rx-worm{color:#fb7185;display:inline-flex;align-items:center;justify-content:center}body .rx-q.rx-worm .ri{width:24px;height:24px;stroke-width:2.1}"
       "body .pr-line{gap:4px}body .pr-emos{font-size:13px;letter-spacing:-1px}body .pr-w{display:inline-flex;align-items:center;gap:2px;color:#fda4af}"
       "body .pr-ic .ri{width:14px;height:14px;display:block}body .pr-w .pr-ic{color:#fb7185}"
       "body .pr-wrap{padding:4px 2px 8px}body .pr-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:2px 0 10px}"
       "body .pr-tab{display:inline-flex;align-items:center;gap:4px;height:28px;padding:0 11px;border-radius:999px;border:1px solid rgba(148,163,184,.22);background:rgba(148,163,184,.06);color:#94a3b8;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit}"
       "body .pr-tab.on{background:#c084fc;border-color:#c084fc;color:#14081d}body .pr-list{display:flex;flex-direction:column;gap:6px}"
       "body .pr-did{margin-left:auto;display:inline-flex;align-items:center;gap:7px;font-size:16px;color:#c084fc}body .pr-did .pr-ic .ri{width:16px;height:16px}"
       "body .pr-did .pr-w{font-size:13px;font-weight:700}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
