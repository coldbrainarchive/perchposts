#!/usr/bin/env python3
"""Patch v939 -> v940: easier chirp reactions + who reacted.
- Tapping a chirp opens a quick-react bar above the actions: ❤️ 😂 😮 😢 👍 🪱 and ＋.
- ＋ opens a full emoji picker sheet (emoji-picker-element 1.29.1, self-hosted in /vendor) with search,
  categories, skin tones and recents, plus a "type any emoji" box for anything the list doesn't have.
- The open chirp menu lists who reacted (bird, name in their colour, their emojis).
- Long-press (or right-click) a reaction pill: sheet of who reacted, with tabs per emoji. Desktop hover
  shows the names as a tooltip. Tapping a pill still toggles your reaction.
- A new reaction flies from the bar into its pill, which pops with a glow in your colour (--me).
- Reaction usernames are remembered per browser_id (_rxU) from the room payload, /get-reactions and your
  own reacts."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v939.js'
dst = '_deploy/assets/index-DUcNPOLc-v940.js'
c = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global c
    n = c.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        c = c.replace(old, new)
        print('OK: ' + label)

# Remember who each reaction belongs to
patch('(_rx||[]).forEach(({comment_id:_i,browser_id:_b,emoji:_m})=>{',
      '(_rx||[]).forEach(({comment_id:_i,browser_id:_b,emoji:_m,username:_un})=>{_un&&(_rxU[_b]=_un);',
      'room reactions: names')
patch('(n||[]).forEach(({comment_id:e,browser_id:t,emoji:n})=>{r[e]',
      '(n||[]).forEach(({comment_id:e,browser_id:t,emoji:n,username:_un})=>{_un&&(_rxU[t]=_un);r[e]',
      'get-reactions: names')
patch('let a=n||E||Qn()?.username||null;fetch(`${R}/react-comment`',
      'let a=n||E||Qn()?.username||null;a&&(_rxU[r]=a);fetch(`${R}/react-comment`',
      'own react: name')

# Chirp component state for the who-reacted sheet
patch('[_birdOpen,_setBirdOpen]=(0,_.useState)(!1),[_birdStats,',
      '[_birdOpen,_setBirdOpen]=(0,_.useState)(!1),[_rxW,_setRxW]=(0,_.useState)(null),[_birdStats,',
      'chirp: sheet state')

# Pills: names tooltip, long-press, pop
patch('className:`chat-reaction-pill${n.includes(C)?` mine`:``}`,onClick:()=>c&&c(e.id,t),children:[t,',
      'className:`chat-reaction-pill${n.includes(C)?` mine`:``}`,"data-emoji":t,title:_rxNames(n).join(`, `),'
      'onPointerDown:ev=>_rxLPStart(ev,()=>_setRxW(t)),onPointerUp:_rxLPEnd,onPointerLeave:_rxLPEnd,onPointerCancel:_rxLPEnd,'
      'onContextMenu:ev=>{ev.preventDefault();_rxLPEnd();_rxF=Date.now();_setRxW(t)},'
      'onClick:()=>{if(_rxLPFired())return;let _m=n.includes(C);c&&c(e.id,t);_m||_rxPop(e.id,t,null)},children:[t,',
      'pills')

# Menu: quick bar on top, React button gone, who list underneath
patch('v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,children:[',
      'v&&c&&_rxBar(e.id,c,E,C,()=>y(!1)),v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,children:[',
      'menu: quick bar')
patch('c&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:D,children:`React`}),', '',
      'menu: drop React button')
patch('children:`Delete`})]}),b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`',
      'children:`Delete`})]}),v&&ee.length>0&&_rxWho(ee,null),b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`',
      'menu: who list')
patch(',_birdOpen?(0,L.jsxs)(`div`,{onClick:()=>{_setBirdOpen(!1);',
      ',_rxW?_rxSheet(ee,_rxW,_setRxW):null,_birdOpen?(0,L.jsxs)(`div`,{onClick:()=>{_setBirdOpen(!1);',
      'who sheet')

JS = r'''
var _rxU={};
const _RXQ=[`❤️`,`😂`,`😮`,`😢`,`👍`,`🪱`],_RXV=`/vendor/emoji-picker-1.29.1/`;
function _rxNames(ids){return ids.map(b=>_rxU[b]||`Anon`)}
function _rxGroup(ee,only){const m=new Map();
 for(const[q,ids]of ee){if(only&&only!==`all`&&q!==only)continue;
  for(const b of ids){const n=_rxU[b]||null,k=n||`#`+b;if(!m.has(k))m.set(k,{name:n,qs:[]});m.get(k).qs.push(q)}}
 return[...m.values()]}
function _rxFace(name,sz){
 if(!name||name===`Extinct Bird`)return{col:`#6b7280`,el:(0,L.jsx)(`span`,{style:{fontSize:sz,lineHeight:1,filter:`grayscale(1) opacity(.75)`},children:`🐦`})};
 const l=name.toLowerCase(),adm=_adminUsers.has(l),b=Jn({username:name,browser_id:null,is_admin:adm,is_mod:_modUsers.has(l)})||{};
 const col=adm?`#ffffff`:_modUsers.has(l)?`#c084fc`:Hn(null,name);
 const el=b.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:sz+3,height:sz+3,objectFit:`contain`}})
  :(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`,justifyContent:`center`,fontSize:sz,lineHeight:1},children:[(0,L.jsx)(`span`,{style:b.f?{filter:b.f}:{},children:b.e||`🐦`}),...(b.s?_spEls(b.s,sz):[])]});
 return{col,el}}
function _rxRow(r,i){const f=_rxFace(r.name,16),c=f.col;
 return(0,L.jsxs)(`div`,{className:`rx-row`,style:{background:`color-mix(in srgb, ${c} 9%, #15171d)`,borderColor:`color-mix(in srgb, ${c} 22%, transparent)`},children:[
  (0,L.jsx)(`span`,{className:`rx-av`,style:{background:`color-mix(in srgb, ${c} 24%, #1b1d24)`,borderColor:`color-mix(in srgb, ${c} 40%, transparent)`},children:f.el}),
  (0,L.jsx)(`span`,{className:`rx-nm`,style:{color:c===`#ffffff`?`#e5e7eb`:c},children:r.name||`Anon`}),
  (0,L.jsx)(`span`,{className:`rx-qs`,children:r.qs.join(` `)})]},i)}
function _rxWho(ee,only){const rows=_rxGroup(ee,only);if(!rows.length)return null;
 return(0,L.jsxs)(`div`,{className:`rx-who`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(`div`,{className:`rx-who-lb`,children:`Reactions`}),...rows.map(_rxRow)]})}
function _rxSheet(ee,sel,set){const tot=ee.reduce((a,[,ids])=>a+ids.length,0),cur=sel===`all`||ee.some(([q])=>q===sel)?sel:`all`;
 const tab=(k,lb)=>(0,L.jsx)(`button`,{type:`button`,className:`rx-tab${cur===k?` on`:``}`,onClick:()=>set(k),children:lb},k);
 return(0,L.jsx)(`div`,{className:`rx-ov`,onClick:ev=>{ev.stopPropagation();set(null)},children:(0,L.jsxs)(`div`,{className:`rx-sheet`,onClick:ev=>ev.stopPropagation(),children:[
  (0,L.jsx)(`div`,{className:`rx-grab`}),
  (0,L.jsxs)(`div`,{className:`rx-tabs`,children:[tab(`all`,`All ${tot}`),...ee.map(([q,ids])=>tab(q,`${q} ${ids.length}`))]}),
  (0,L.jsx)(`div`,{className:`rx-list`,children:_rxGroup(ee,cur).map(_rxRow)})]})})}
function _rxBar(id,react,E,me,close){
 return(0,L.jsxs)(`div`,{className:`rx-bar`,onClick:ev=>ev.stopPropagation(),children:[
  ..._RXQ.map(q=>{const mine=(E[q]||[]).includes(me);
   return(0,L.jsx)(`button`,{type:`button`,className:`rx-q${mine?` mine`:``}`,"aria-label":`React ${q}`,onClick:ev=>{const r=ev.currentTarget.getBoundingClientRect();react(id,q);close();mine||_rxPop(id,q,r)},children:q},q)}),
  (0,L.jsx)(`button`,{type:`button`,className:`rx-q rx-plus`,"aria-label":`More emoji`,onClick:()=>{close();
   if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}
   _rxPick(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)})},children:`+`})]})}
let _rxT=null,_rxF=0;
function _rxLPStart(ev,fn){clearTimeout(_rxT);_rxT=setTimeout(()=>{_rxF=Date.now();try{navigator.vibrate&&navigator.vibrate(10)}catch(e){}fn()},450)}
function _rxLPEnd(){clearTimeout(_rxT)}
function _rxLPFired(){if(_rxF&&Date.now()-_rxF<1500){_rxF=0;return!0}return!1}
function _rxPop(id,q,from){let n=0;const go=()=>{
 const p=document.querySelector(`[data-comment-id="${CSS.escape(String(id))}"] .chat-reaction-pill[data-emoji="${CSS.escape(q)}"]`);
 if(!p){if(++n<20)requestAnimationFrame(go);return}
 const pop=()=>{p.classList.remove(`rx-pop`);void p.offsetWidth;p.classList.add(`rx-pop`);setTimeout(()=>p.classList.remove(`rx-pop`),600)};
 if(!from||matchMedia(`(prefers-reduced-motion: reduce)`).matches)return pop();
 const t=p.getBoundingClientRect(),x=from.left+from.width/2,y=from.top+from.height/2,f=document.createElement(`span`);
 f.className=`rx-fly`;f.textContent=q;f.style.left=x+`px`;f.style.top=y+`px`;document.body.appendChild(f);
 requestAnimationFrame(()=>requestAnimationFrame(()=>{f.style.transform=`translate(${t.left+13-x}px,${t.top+t.height/2-y}px) scale(.45)`}));
 setTimeout(()=>{f.remove();pop()},380)};requestAnimationFrame(go)}
function _rxFirstEmoji(s){const ok=g=>/\p{Extended_Pictographic}|\p{Regional_Indicator}|⃣/u.test(g);
 try{if(window.Intl&&Intl.Segmenter){for(const{segment:g}of new Intl.Segmenter().segment(s))if(ok(g))return g;return null}}catch(e){}
 return[...s].find(ok)||null}
let _rxMod=null;
function _rxPick(cb){
 const ov=document.createElement(`div`);ov.className=`rx-pick-ov`;
 const sh=document.createElement(`div`);sh.className=`rx-pick`;
 const hd=document.createElement(`div`);hd.className=`rx-pick-hd`;
 const tt=document.createElement(`span`);tt.textContent=`React with any emoji`;
 const x=document.createElement(`button`);x.type=`button`;x.className=`rx-pick-x`;x.textContent=`✕`;x.setAttribute(`aria-label`,`Close`);
 hd.append(tt,x);
 const host=document.createElement(`div`);host.className=`rx-pick-host`;
 const ld=document.createElement(`div`);ld.className=`rx-pick-msg`;ld.textContent=`Loading emoji…`;host.append(ld);
 const kb=document.createElement(`input`);kb.className=`rx-kb`;kb.type=`text`;kb.setAttribute(`inputmode`,`emoji`);kb.setAttribute(`enterkeyhint`,`done`);
 kb.setAttribute(`autocomplete`,`off`);kb.setAttribute(`autocorrect`,`off`);kb.placeholder=`⌨️  Or type any emoji from your keyboard`;
 sh.append(hd,host,kb);ov.append(sh);
 let shut=!1;
 const close=()=>{if(shut)return;shut=!0;document.removeEventListener(`keydown`,esc);ov.classList.remove(`in`);setTimeout(()=>ov.remove(),200)};
 const done=q=>{close();cb(q)};
 const esc=e=>{if(e.key===`Escape`)close()};
 document.addEventListener(`keydown`,esc);
 x.onclick=close;ov.onclick=e=>{if(e.target===ov)close()};
 kb.oninput=()=>{const g=_rxFirstEmoji(kb.value);if(g){kb.blur();done(g)}else if(kb.value&&!/[\uD800-\uDBFF️‍]$/.test(kb.value))kb.value=``};
 document.body.append(ov);requestAnimationFrame(()=>requestAnimationFrame(()=>ov.classList.add(`in`)));
 (_rxMod||(_rxMod=import(_RXV+`index.js`))).then(()=>{if(shut)return;const p=document.createElement(`emoji-picker`);
  p.className=`dark`;p.setAttribute(`data-source`,_RXV+`emoji-data.json`);p.addEventListener(`emoji-click`,e=>{e.detail&&e.detail.unicode&&done(e.detail.unicode)});host.replaceChildren(p)})
 .catch(()=>{_rxMod=null;ld.textContent=`Couldn't load the emoji list. Type one below instead.`})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.chat-reactions .chat-reaction-pill{-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;touch-action:manipulation}
.chat-reactions .chat-reaction-pill.mine{border-color:var(--me,#c084fc);background:color-mix(in srgb,var(--me,#c084fc) 16%,transparent)}
.chat-reaction-pill.rx-pop{animation:rxPop .5s cubic-bezier(.3,1.6,.5,1)}
@keyframes rxPop{0%{transform:scale(.6)}45%{transform:scale(1.28);box-shadow:0 0 0 2px color-mix(in srgb,var(--me,#c084fc) 45%,transparent),0 0 12px color-mix(in srgb,var(--me,#c084fc) 70%,transparent)}100%{transform:scale(1)}}
.rx-fly{position:fixed;z-index:9999;pointer-events:none;font-size:26px;line-height:1;margin:-13px 0 0 -13px;transition:transform .38s cubic-bezier(.3,.7,.4,1)}
.rx-bar{display:flex;align-items:center;justify-content:space-between;gap:4px;padding:8px 12px 2px;background:#1e2530;border-top:1px solid rgba(148,163,184,.1)}
.rx-q{flex:1 1 0;min-width:0;max-width:46px;height:38px;border-radius:999px;border:1px solid rgba(148,163,184,.16);background:rgba(148,163,184,.06);font-size:21px;line-height:1;padding:0;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .12s,background .12s;-webkit-tap-highlight-color:transparent}
.rx-q:active{transform:scale(1.18)}
@media (hover:hover){.rx-q:hover{transform:scale(1.12);background:rgba(148,163,184,.12)}}
.rx-q.mine{border-color:var(--me,#c084fc);background:color-mix(in srgb,var(--me,#c084fc) 18%,transparent)}
.rx-plus{font-size:20px;font-weight:600;color:#94a3b8}
.rx-who{display:flex;flex-direction:column;gap:5px;padding:4px 12px 10px;background:#1e2530}
.rx-who-lb{font-size:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#64748b;padding:2px 2px 0}
.rx-row{display:flex;align-items:center;gap:9px;padding:4px 12px 4px 4px;border-radius:999px;border:1px solid transparent;min-height:34px;box-sizing:border-box}
.rx-av{width:28px;height:28px;flex-shrink:0;border-radius:999px;border:1px solid transparent;display:flex;align-items:center;justify-content:center}
.rx-nm{flex:1;min-width:0;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:left}
.rx-qs{flex-shrink:0;font-size:16px;letter-spacing:2px;line-height:1}
.rx-ov{position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.55);display:flex;align-items:flex-end;justify-content:center;animation:rxFade .18s ease-out}
.rx-sheet{width:100%;max-width:480px;max-height:70vh;display:flex;flex-direction:column;background:#161920;border-radius:18px 18px 0 0;box-shadow:0 -8px 40px rgba(0,0,0,.4);padding:0 0 calc(18px + env(safe-area-inset-bottom));animation:rxUp .22s cubic-bezier(.2,.8,.3,1)}
.rx-grab{width:36px;height:4px;border-radius:999px;background:#3a3f4b;margin:9px auto 6px}
.rx-tabs{display:flex;gap:6px;padding:4px 14px 10px;overflow-x:auto;scrollbar-width:none}
.rx-tabs::-webkit-scrollbar{display:none}
.rx-tab{flex-shrink:0;height:30px;padding:0 12px;border-radius:999px;border:1px solid #2e303a;background:transparent;color:#94a3b8;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}
.rx-tab.on{border-color:#c084fc;color:#e9d5ff;background:rgba(192,132,252,.14)}
.rx-list{display:flex;flex-direction:column;gap:6px;padding:0 14px;overflow-y:auto}
.rx-list .rx-row{min-height:42px;padding:5px 14px 5px 5px}
.rx-list .rx-av{width:32px;height:32px}
.rx-list .rx-nm{font-size:13px}
.rx-list .rx-qs{font-size:18px}
.rx-pick-ov{position:fixed;inset:0;z-index:1001;background:rgba(0,0,0,0);display:flex;align-items:flex-end;justify-content:center;transition:background .2s}
.rx-pick-ov.in{background:rgba(0,0,0,.55)}
.rx-pick{width:100%;max-width:480px;background:#161920;border-radius:18px 18px 0 0;box-shadow:0 -8px 40px rgba(0,0,0,.4);padding:0 0 calc(12px + env(safe-area-inset-bottom));transform:translateY(100%);transition:transform .24s cubic-bezier(.2,.8,.3,1)}
.rx-pick-ov.in .rx-pick{transform:none}
.rx-pick-hd{display:flex;align-items:center;justify-content:space-between;padding:12px 14px 8px;color:#e2e8f0;font-size:14px;font-weight:800}
.rx-pick-x{width:30px;height:30px;border-radius:999px;border:1px solid #2e303a;background:transparent;color:#94a3b8;font-size:13px;cursor:pointer}
.rx-pick-host{height:min(360px,52vh);display:flex;padding:0 8px}
.rx-pick-msg{margin:auto;color:#64748b;font-size:13px;padding:0 20px;text-align:center}
.rx-pick emoji-picker{width:100%;height:100%;--background:#161920;--border-color:#2e303a;--border-size:0;--indicator-color:var(--me,#c084fc);--input-border-color:#2e303a;--input-font-color:#e2e8f0;--input-placeholder-color:#64748b;--input-border-radius:999px;--outline-color:#c084fc;--button-active-background:#2a2d38;--button-hover-background:#232631;--category-font-color:#94a3b8;--emoji-size:1.55rem;--emoji-padding:.4rem;--num-columns:8}
.rx-kb{display:block;width:calc(100% - 28px);margin:8px 14px 0;height:38px;box-sizing:border-box;padding:0 14px;border-radius:999px;border:1px solid #2e303a;background:#1b1d24;color:#e2e8f0;font-size:16px;outline:none;font-family:inherit}
.rx-kb:focus{border-color:#c084fc}
.rx-kb::placeholder{color:#64748b;font-size:13px}
@keyframes rxFade{from{opacity:0}}
@keyframes rxUp{from{transform:translateY(100%)}}
@media (prefers-reduced-motion: reduce){.rx-ov,.rx-sheet,.chat-reaction-pill.rx-pop{animation:none}.rx-pick,.rx-pick-ov{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''

if errors:
    print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c + JS)
print('Wrote ' + dst)
