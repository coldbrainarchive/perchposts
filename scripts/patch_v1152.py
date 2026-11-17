#!/usr/bin/env python3
"""Patch v1148 -> v1152 (v1149-v1151 were unreleased drafts):
- The chirp preview menu's "Flaps & worms" is called "Flaps" (it still lists worms too).
- The post page's worm pill always shows (🪱 0 too; not on bot posts). Tapping it opens the "Worm wallet": like the
  emoji sheet, the screen dims, the post lifts to the top, and a sheet shows your worms with − / + / Give.
  On your own post it shows your balance and that you can't give worms to yourself.
- Giving worms moves out of the Flaps dropdown (its "Give worms" button is gone)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1148.js'
dst = '_deploy/assets/index-DUcNPOLc-v1152.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

WALLET = r'''function _wormWallet(id,own){if(document.querySelector(`.ww-ov`))return;
 const src=document.querySelector(`.feed-post-card`);const ov=document.createElement(`div`);ov.className=`ri-ov ww-ov`;
 const top=document.createElement(`div`);top.className=`ri-top ww-top`;
 if(src){const k=src.cloneNode(!0);k.querySelectorAll(`[id]`).forEach(x=>x.removeAttribute(`id`));const wr=document.createElement(`div`);wr.className=`ww-post`;wr.style.width=Math.min(src.getBoundingClientRect().width||340,innerWidth-24)+`px`;wr.append(k);top.append(wr)}
 const sh=document.createElement(`div`);sh.className=`ri-sheet ww-sheet`;sh.setAttribute(`role`,`dialog`);sh.setAttribute(`aria-label`,`Worm wallet`);
 sh.innerHTML=`<div class="ri-worms ww-worms"><div class="pp-pick-worm"><span class="pp-ic pp-worm">${_ppIco(`WORM`)}</span><span class="pp-pick-wl">Worm wallet</span>`+(own?``:`<button type="button" class="pp-pick-st" aria-label="Fewer">−</button><b class="pp-pick-n">1</b><button type="button" class="pp-pick-st" aria-label="More">+</button><button type="button" class="pp-pick-give">Give 1</button>`)+`</div><div class="pp-pick-bal"></div></div>`;
 ov.append(top,sh);document.body.append(ov);requestAnimationFrame(()=>ov.classList.add(`in`));
 let shut=!1,cnt=1,bal=_ppWorm.bal();const bl=sh.querySelector(`.pp-pick-bal`);
 const close=()=>{if(shut)return;shut=!0;document.removeEventListener(`keydown`,esc);ov.classList.remove(`in`);setTimeout(()=>ov.remove(),220)};
 const esc=e=>{if(e.key===`Escape`)close()};document.addEventListener(`keydown`,esc);
 ov.addEventListener(`click`,e=>{if(e.target===ov||e.target.closest(`.ww-top`))close()});
 const have=()=>bal==null?`Counting your worms…`:`You have ${bal} worm${bal===1?``:`s`}`;
 const upd=()=>{if(own){bl.textContent=have()+` · You can't give worms to your own post`;return}bl.textContent=bal===0?`You don't have any worms to give`:have();
  if(bal!=null&&cnt>Math.max(1,bal))cnt=Math.max(1,bal);const[mn,pl]=sh.querySelectorAll(`.pp-pick-st`),go=sh.querySelector(`.pp-pick-give`);
  sh.querySelector(`.pp-pick-n`).textContent=cnt;go.textContent=`Give ${cnt}`;go.disabled=bal===0;mn.disabled=cnt<=1;pl.disabled=bal!=null&&cnt>=bal||cnt>=50};
 if(!own){const[mn,pl]=sh.querySelectorAll(`.pp-pick-st`);mn.onclick=()=>{cnt=Math.max(1,cnt-1);upd()};pl.onclick=()=>{cnt=Math.min(50,bal==null?cnt+1:Math.min(bal,cnt+1));upd()};
  sh.querySelector(`.pp-pick-give`).onclick=()=>{if(bal===0)return;if(_ppWorm.give(`p`,id,cnt))close()}}
 upd();if(localStorage.getItem(`auth_token`))_ppWorm.loadBal().then(v=>{bal=v;upd()});else{bl.textContent=`Sign in to give worms`}}
'''
patch("function _PFTabs({u,on}){", WALLET + "function _PFTabs({u,on}){", 'worm wallet')
# post page pill: always shown, opens the wallet
patch("function _PostRespLine({id,pv,setCpm}){", "function _PostRespLine({id,pv,setCpm,own}){", 'pill knows own')
patch("if(!nw&&!open)return null;", "", 'pill shows 0 too')
patch("onClick:ev=>{ev.preventDefault();ev.stopPropagation();if(pv){setCpm(`react`);setTimeout(()=>document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`}),50)}else setOpen(!0)},children:[",
      "onClick:ev=>{ev.preventDefault();ev.stopPropagation();if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}_wormWallet(id,own)},children:[", 'pill opens the wallet')
patch("!c?.is_huddle&&c&&(0,L.jsx)(_PostRespLine,{id:c.id,pv:_pv,setCpm:_setCpm}),",
      "!c?.is_huddle&&c&&!_ppIsBot(c)&&(0,L.jsx)(_PostRespLine,{id:c.id,pv:_pv,setCpm:_setCpm,own:_ppOwn(c.username)}),", 'post page passes own; no pill on bots')
# menu label; the dropdown no longer gives worms
patch("const _CPL={react:`🪽 Flaps & worms`,", "const _CPL={react:`🪽 Flaps`,", 'menu says Flaps')
patch(",bot?null:(0,L.jsxs)(`button`,{type:`button`,className:`wg-open`+(gop?` on`:``),\"aria-expanded\":gop,onClick:ev=>{ev.stopPropagation();setGop(!gop)},children:[`Give worms`,(0,L.jsx)(`span`,{className:`wg-chev`,children:`⌄`})]},`give`)]}),\n  gop&&!bot?(0,L.jsx)(_WormGive,{id,kind:`p`,bare:1}):null,",
      "]}),", 'no Give worms in the dropdown')
css = ("body .ww-ov{flex-direction:column;align-items:center}"
       "body .ww-top{width:100%;box-sizing:border-box;flex:1;min-height:0;display:flex;align-items:flex-end;justify-content:center;padding:calc(env(safe-area-inset-top) + 16px) 16px 16px;overflow:hidden;cursor:pointer}"
       "body .ww-post{max-height:100%;overflow:hidden;pointer-events:none;border-radius:20px;box-shadow:0 12px 40px rgba(0,0,0,.6)}body .ww-post .feed-post-card{margin:0!important}"
       "body .ww-worms{padding:14px 18px 10px}body .ww-worms .pp-pick-worm{border-top:0}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
n=c.count('<span class="pp-pick-wl">Give worms</span>');print('worm panels to rename:',n)
c=c.replace('<span class="pp-pick-wl">Give worms</span>','<span class="pp-pick-wl">Worm wallet</span>')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
